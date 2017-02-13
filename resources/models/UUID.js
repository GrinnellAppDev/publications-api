module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "UUID",
    description: "A universally unique identifier string",
    type: "string",
    pattern: "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-" +
             "[a-fA-F0-9]{12}$",
});
