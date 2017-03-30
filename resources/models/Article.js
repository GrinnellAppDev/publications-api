module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "Article",
    description: "Full article with all of its information",
    type: "object",
    required: ["id", "publication", "datePublished", "dateEdited", "title",
               "content", "authors"],
    additionalProperties: false,
    properties: Object.assign(require("./ShortArticle").schema().properties,
                              require("./ArticleCreate").schema().properties, {
        dateEdited: {
            type: "number",
            description: "The timestamp the article was last edited as a " +
                         "Unix timestamp in milliseconds",
        },
    }),
});
