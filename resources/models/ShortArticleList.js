module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "ShortArticleList",
    description: "A list of article briefs",
    type: "object",
    required: ["items"],
    additionalProperties: false,
    properties: {
        items: {
            type: "array",
            items: require("./ShortArticle").schema(),
        },
    },
});
