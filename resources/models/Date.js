module.exports.schema = () => ({
    $schema: "http://json-schema.org/draft-04/schema#",
    title: "Date",
    description: "A string-encoded date",
    type: "string",
    pattern: "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}.\\d{6}$",
});
