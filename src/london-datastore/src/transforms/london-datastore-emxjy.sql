-- provisional fixed-schema pass-through; regenerate after model-verify with hardened compile-transforms
SET arrow_large_buffer_size=true;

SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_url",
    "member_path",
    "sheet_name",
    "source_row_number",
    "data_json"
FROM "london-datastore-emxjy"
