const { Router } = require("express")
const querystring = require("querystring")

const {
    runWithDB,
    validateRequest,
    base64ToId,
    idToBase64,
    HTTPError
} = require("./util")

module.exports = Router()
    /**
     * @swagger
     *  /publications:
     *    get:
     *      summary: Get a list of all publications
     *      parameters:
     *        - name: pageSize
     *          in: query
     *          description: Maximum number of items per response
     *          schema:
     *            type: integer
     *            default: 10
     *        - name: pageToken
     *          in: query
     *          description: Token representing a particular page of results
     *          schema:
     *            type: string
     *      responses:
     *        200:
     *          description: An array of publications
     *          headers:
     *            Link:
     *              schema:
     *                type: string
     *              description: >
     *                Standard HTTP Link header. All URIs relative to the /publications endpoint.
     *          content:
     *            application/json:
     *              schema:
     *                type: array
     *                items:
     *                  $ref: "#/components/schemas/Publication"
     *        400:
     *          $ref: "#/components/responses/BadRequest"
     */
    .get("/", (request, response) =>
        runWithDB(async db => {
            validateRequest(request, {
                querySchemaProps: {
                    pageSize: { type: "string", pattern: "^\\d+$" },
                    pageToken: { type: "string", format: "urlsafeBase64" }
                }
            })

            const publicationsCollection = db.collection("publications")

            /** @type {number} */ const pageSize = +request.query.pageSize || 10
            /** @type {string} */ const pageToken =
                request.query.pageToken || null

            let pageTokenValue = null
            if (pageToken) {
                try {
                    pageTokenValue = base64ToId(pageToken)
                } catch (error) {
                    throw new HTTPError(400, "Invalid pageToken.")
                }
            }

            const query = { _userId: request.authorizedUser }
            const allPublications = pageToken
                ? publicationsCollection.find({
                      ...query,
                      _id: { $lte: pageTokenValue }
                  })
                : publicationsCollection.find(query)

            const readPublications = await allPublications
                .sort("_id", -1)
                .limit(pageSize + 1)
                .toArray()

            const items = readPublications
                .slice(0, pageSize)
                .map(publication => ({
                    _id: publication._id,
                    isComplete: publication.isComplete,
                    text: publication.text
                }))

            const nextPageFirstPublication = readPublications[pageSize]
            if (nextPageFirstPublication) {
                response.links({
                    next: `publications?${querystring.stringify({
                        ...request.query,
                        pageToken: idToBase64(nextPageFirstPublication._id)
                    })}`
                })
            }

            response.status(200).send(items)
        })
    )
