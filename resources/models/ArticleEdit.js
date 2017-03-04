module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "ArticleEdit",
    description: "The mutable fields of an article",
    additionalProperties: false,
    properties: require("./ArticleCreate").schema().properties,
});
