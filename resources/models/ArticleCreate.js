module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "ArticleCreate",
    description: "The mutable fields of an article required for creation",
    additionalProperties: false,
    required: ["title", "authors", "content"],
    properties: {
        headerImage: Object.assign(require("./URL").schema(), {
            description: "The URL of the header image",
        }),
        title: {
            type: "string",
            description: "The headline of the article",
        },
        content: {
            type: "string",
            description: "The full text of the article formatted with markdown",
        },
        authors: {
            type: "array",
            description: "A list of all collaborators on the article",
            items: require("./Author").schema(),
        },
    }
});