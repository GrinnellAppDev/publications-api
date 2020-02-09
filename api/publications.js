const { Router } = require("express")
const querystring = require("querystring")

const {
  runWithDB,
  validateRequest,
  base64ToId,
  base64ToNumber,
  idToBase64,
  numberToBase64,
  HTTPError
} = require("./util")
const publicationsAvailable = require("./publications-available")

module.exports = Router()
  /**
   * @swagger
   *  /publications:
   *    get:
   *      summary: Get a list of all publications
   *      responses:
   *        200:
   *          description: A list of publications
   *          content:
   *            application/json:
   *              schema:
   *                type: object
   *                properties:
   *                  items:
   *                    type: array
   *                    items:
   *                      $ref: "#/components/schemas/Publication"
   */
  .get("/", (request, response) => {
    response.status(200).send({
      items: publicationsAvailable.items
    })
  })

  /**
   * @swagger
   *  /publications/{publicationId}/articles:
   *    get:
   *      summary: Get a list of article thumbnails in a particular publication
   *      parameters:
   *        - name: publicationId
   *          in: path
   *          required: true
   *          description: The publication to query
   *          schema:
   *            type: string
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
   *          description: >
   *            A list of articles. This is **not** trusted data. The structure is
   *            guaranteed, but the contents of the fields could be crafted by an
   *            attacker, so take care.
   *          headers:
   *            Link:
   *              schema:
   *                type: string
   *              description: >
   *                Standard HTTP Link header. All URIs relative to the /publications endpoint.
   *          content:
   *            application/json:
   *              schema:
   *                type: object
   *                properties:
   *                  items:
   *                    type: array
   *                    items:
   *                      $ref: "#/components/schemas/ArticleThumbnail"
   *                  nextPageToken:
   *                    type: string
   *                    nullable: true
   *        400:
   *          $ref: "#/components/responses/BadRequest"
   *        404:
   *          $ref: "#/components/responses/NotFound"
   */
  .get("/:publicationId/articles", (request, response) =>
    runWithDB(async db => {
      validateRequest(request, {
        paramSchemaProps: {
          publicationId: { type: "string" }
        },
        querySchemaProps: {
          pageSize: { type: "string", pattern: "^\\d+$" },
          pageToken: { type: "string", format: "urlsafeBase64" }
        }
      })

      const articlesCollection = db.collection("articles")

      /** @type {number} */ const pageSize = +request.query.pageSize || 10
      /** @type {string} */ const pageToken = request.query.pageToken || null
      /** @type {string} */ const publicationId = request.params.publicationId

      let pageTokenValue = 0
      if (pageToken) {
        try {
          pageTokenValue = base64ToNumber(pageToken)
        } catch (error) {
          throw new HTTPError(400, "Invalid pageToken.")
        }
      }

      if (!publicationsAvailable.items.some(({ id }) => id === publicationId)) {
        throw new HTTPError(404, `No publication with id "${publicationId}".`)
      }

      await articlesCollection.createIndex({
        publication: 1,
        datePublished: -1
      })
      const query = { publication: publicationId }
      const articles = pageToken
        ? articlesCollection.find({
            ...query,
            datePublished: { $lte: pageTokenValue }
          })
        : articlesCollection.find(query)

      const limitedArticles = await articles
        .sort("datePublished", -1)
        .limit(pageSize + 1)
        .toArray()

      const items = limitedArticles.slice(0, pageSize).map(article => ({
        id: article.id,
        publication: article.publication,
        title: article.title,
        datePublished: article.datePublished,
        authors: article.authors.map(author => ({
          ...author,
          email: author.email || null
        })),
        readTimeMinutes: article.readTimeMinutes,
        headerImage: article.headerImage || null
      }))

      const nextPageFirstArticle = limitedArticles[pageSize]
      let nextPageToken = null

      if (nextPageFirstArticle) {
        // TODO: mash in the id for unique ordering
        nextPageToken = numberToBase64(nextPageFirstArticle.datePublished)

        response.links({
          next: `articles?${querystring.stringify({
            ...request.query,
            pageToken: nextPageToken
          })}`
        })
      }

      response.status(200).send({ items, nextPageToken })
    })
  )

  /**
   * @swagger
   *  /publications/{publicationId}/articles/{articleId}:
   *    get:
   *      summary: Show detailed information on a particular article.
   *      parameters:
   *        - name: publicationId
   *          in: path
   *          required: true
   *          description: The publication to query
   *          schema:
   *            type: string
   *        - name: articleId
   *          in: path
   *          required: true
   *          description: The article to be accessed
   *          schema:
   *            type: string
   *      responses:
   *        200:
   *          description: >
   *            A single article. This is **not** trusted data. The structure is
   *            guaranteed, but the contents of the fields could be crafted by an
   *            attacker, so take care.
   *          content:
   *            application/json:
   *              schema:
   *                $ref: "#/components/schemas/Article"
   *        400:
   *          $ref: "#/components/responses/BadRequest"
   *        404:
   *          $ref: "#/components/responses/NotFound"
   */
  .get("/:publicationId/articles/:articleId", (request, response) =>
    runWithDB(async db => {
      validateRequest(request, {
        paramSchemaProps: {
          publicationId: { type: "string" },
          articleId: { type: "string" }
        }
      })

      const articlesCollection = db.collection("articles")

      /** @type {string} */ const publicationId = request.params.publicationId
      /** @type {string} */ const articleId = request.params.articleId

      if (!publicationsAvailable.items.some(({ id }) => id === publicationId)) {
        throw new HTTPError(404, `No publication with id "${publicationId}".`)
      }

      await articlesCollection.createIndex(
        { publication: 1, id: 1 },
        { unique: true }
      )
      const article = await articlesCollection
        .find({
          publication: publicationId,
          id: articleId
        })
        .limit(1)
        .next()

      if (!article) {
        throw new HTTPError(
          404,
          `No article with id "${articleId}" in publication "${publicationId}".`
        )
      }

      response.status(200).send({
        id: article.id,
        url: article.url,
        publication: article.publication,
        title: article.title,
        datePublished: article.datePublished,
        dateEdited: article.dateEdited,
        authors: article.authors.map(author => ({
          ...author,
          email: author.email || null
        })),
        headerImage: article.headerImage || null,
        content: article.content,
        readTimeMinutes: article.readTimeMinutes
      })
    })
  )
