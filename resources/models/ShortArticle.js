module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "ShortArticle",
    description: "Shortened article with only the information needed to show " +
                 "it in a listview",
    required: ["id", "publication", "datePublished", "title", "authors",
               "readTimeMinutes"],
    additionalProperties: false,
    properties: {
        id: Object.assign(require("./UUID").schema(), {
            description: "The unique ID of the article",
        }),
        publication: Object.assign(require("./UUID").schema(), {
            description: "The unique ID of the article's publication",
        }),
        datePublished: {
            type: "number",
            description: "The timestamp the article was published as a Unix " +
                         "timestamp in milliseconds",
        },
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
        readTimeMinutes: {
            type: "number",
            description: "The amount of time in minutes it should take the " +
                         "average college student to read the article",
        },
    },
});
