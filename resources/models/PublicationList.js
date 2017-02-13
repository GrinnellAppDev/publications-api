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
    },
});
