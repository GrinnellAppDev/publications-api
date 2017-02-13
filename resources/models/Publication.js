module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "Publication",
    description: "A publication resource representation without children",
    required: ["id", "name"],
    additionalProperties: false,
    properties: {
        id: Object.assign(require("./UUID").schema(), {
            description: "The unique id of the publication",
        }),
        name: {
            type: "string",
            description: "The name of the publication",
        },
    },
});
