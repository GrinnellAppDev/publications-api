module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "PublicationList",
    description: "A list of publications",
    type: "object",
    required: ["items"],
    additionalProperties: false,
    properties: {
        items: {
            type: "array",
            items: require("./Publication").schema(),
        },
        nextPageToken: {
            type: "string",
            description: "A token to pass to the next request.  Will be " +
                         "absent if there is no next page",
        },
    },
});
