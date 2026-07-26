-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "marshal_last_name",
    "assessment_fee",
    "adjusted_gross_fee_poundage",
    "net_income_marshals_office"
FROM "nyc-open-data-7ewi-9cdf"
