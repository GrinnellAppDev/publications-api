module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "Author",
    description: "Shortened article with only the information needed to show " +
                 "it in a listview",
    required: ["name"],
    additionalProperties: false,
    properties: {
        name: {
            type: "string",
            description: "The full name of the author",
        },
        email: Object.assign(require("./Email").schema(), {
            description: "The preferred email of the author"
        }),
    },
});
