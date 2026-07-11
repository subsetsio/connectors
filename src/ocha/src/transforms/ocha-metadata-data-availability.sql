-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows enumerate HAPI availability by geography and thematic category; hapi_updated_date is the batch index update timestamp, not the observation period of every underlying dataset.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "category",
    "subcategory",
    CAST("hapi_updated_date" AS TIMESTAMP) AS hapi_updated_date
FROM "ocha-metadata-data-availability"
