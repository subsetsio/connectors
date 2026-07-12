-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows come from multiple additional trend table layouts; use table_title and headers to interpret the generic column_1 through column_5 fields before comparing or aggregating values.
SELECT
    "jurisdiction_id",
    "jurisdiction_name",
    "region",
    "table_title",
    "headers",
    "column_1",
    "column_2",
    "column_3",
    "column_4",
    "column_5",
    "country_url"
FROM "world-prison-brief-additional-trend-tables"
