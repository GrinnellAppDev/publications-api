module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "PagingParams",
    description: "URL query parameters for paginated responses.  Note that JSON should not actually be sent in the request, instead send the data as query parameters of the URL, eg. https://example.com/exampleendpoint?pageSize=10&pageToken=fubar",
    type: "object",
    additionalProperties: false,
    properties: {
        pageToken: {
            type: "string",
            description: "A nextPageToken from a previous response",
        },
        pageSize: Object.assign(require("./StringNumber").schema(), {
            description: "The maximum number of entries per response",
        }),
    },
});
