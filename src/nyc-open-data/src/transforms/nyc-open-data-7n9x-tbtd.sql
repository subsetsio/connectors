-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "nta_code",
    "nta_name",
    "ntaabbrev",
    "scenario_code",
    "scenario_name",
    "count",
    "_percent" AS percent
FROM "nyc-open-data-7n9x-tbtd"
