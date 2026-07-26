-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dsny_storm",
    "date_of_report",
    "manhattan",
    "bronx",
    "brooklyn",
    "queens",
    "staten_island",
    "total_tons"
FROM "nyc-open-data-tavr-zknk"
