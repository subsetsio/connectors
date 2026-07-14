-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are site-level phenometric aggregates and should not be combined with individual-level phenometrics or raw status/intensity observations without first aligning the aggregation level.
SELECT
    "json"
FROM "usa-npn-site-phenometrics"
