-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "council_member_name",
    "council_member_id",
    "term_start",
    "term_end",
    "district",
    "office_id"
FROM "nyc-open-data-uvw5-9znb"
