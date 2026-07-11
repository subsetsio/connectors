-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Handler ID" AS handler_id,
    "Handler Name" AS handler_name,
    "Address" AS address,
    "City" AS city,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County" AS county,
    CAST("Latitude" AS DOUBLE) AS latitude,
    CAST("Longitude" AS DOUBLE) AS longitude,
    "Generator Status" AS generator_status,
    "Biennial Report Link" AS biennial_report_link
FROM "instituto-de-estad-sticas-de-puerto-rico-br"
