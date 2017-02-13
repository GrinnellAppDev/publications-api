module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "URL",
    description: "A fully qualified URL",
    type: "string",
    pattern: "^\\w+://[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\." +
             "[a-z]{2,6}\\b[-a-zA-Z0-9@:%_\\+.~#?&//=]*$",
});
