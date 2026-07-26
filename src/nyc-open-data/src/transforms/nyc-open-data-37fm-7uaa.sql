-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_name" AS name,
    "address_1",
    "address_2",
    "city",
    "state",
    "zip_code",
    "phone",
    "_days" AS days,
    "_hours" AS hours,
    "latitude",
    "longitude",
    "community_board",
    "community_council",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-37fm-7uaa"
