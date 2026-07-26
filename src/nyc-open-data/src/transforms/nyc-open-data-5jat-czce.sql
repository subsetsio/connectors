-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acc",
    "sheets",
    "cp_number",
    "map_year",
    "dimensions",
    "map_title_and_information"
FROM "nyc-open-data-5jat-czce"
