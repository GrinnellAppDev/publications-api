module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "Email",
    description: "An email string",
    type: "string",
    pattern: "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
});
