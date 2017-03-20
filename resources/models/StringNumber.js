module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "StringNumber",
    description: "A number represented as a string",
    type: "string",
    pattern: "^\\d+$",
});
