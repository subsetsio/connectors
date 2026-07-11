-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include region and county dimensions; use the intended geography level before aggregating beneficiaries or benefit amounts.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    "region",
    "county",
    CAST("beneficiaries" AS BIGINT) AS beneficiaries,
    CAST("benefit_amounts_dollars" AS BIGINT) AS benefit_amounts_dollars
FROM "new-york-state-department-of-labor-xbjp-8sra"
