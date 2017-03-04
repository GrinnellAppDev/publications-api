module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "ShortArticle",
    description: "Shortened article with only the information needed to show " +
                 "it in a listview",
    required: ["id", "publication", "datePublished", "title", "authors"],
    additionalProperties: false,
    properties: {
        id: Object.assign(require("./UUID").schema(), {
            description: "The unique ID of the article",
        }),
        publication: Object.assign(require("./UUID").schema(), {
            description: "The unique ID of the article's publication",
        }),
        datePublished: Object.assign(require("./Date").schema(), {
            description: "The date and time the article was published",
        }),
        headerImage: Object.assign(require("./URL").schema(), {
            description: "The URL of the header image"
        }),
        title: {
            type: "string",
            description: "The headline of the article",
        },
        authors: {
            type: "array",
            description: "A list of all collaborators on the article",
            items: require("./Author").schema(),
        },
    },
});
