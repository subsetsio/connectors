-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fhfa_id",
    "district",
    "member_name",
    "city",
    "state",
    "zip",
    "mem_type",
    "char_type",
    "cert",
    "fed_id",
    "ncua_id",
    "naic_id",
    "appr_date",
    "mem_date",
    "release_period",
    "source_url"
FROM "fhfa-fhlbank-member-data"
