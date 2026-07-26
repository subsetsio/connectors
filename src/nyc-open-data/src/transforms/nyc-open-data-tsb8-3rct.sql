-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hdrsystem_acceptance_date",
    "vendlegal_name",
    "commitem_total_amt",
    "actgline_description"
FROM "nyc-open-data-tsb8-3rct"
