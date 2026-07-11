-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Subnational corruption records include multiple administrative levels; filter the level column before aggregating or comparing regions.
SELECT
    "iso_code",
    "iso2",
    "iso_num",
    "country",
    "year",
    "datasource",
    "gdlcode",
    "gdlcode_sci",
    "level",
    "region",
    "region_sci",
    "continent",
    "ngrand",
    "npetty",
    "fullsci",
    "sci",
    "grand",
    "petty"
FROM "prio-37"
