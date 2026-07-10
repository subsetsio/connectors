-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are FTC merger enforcement matters; enforcement type and industry are source categories, not mutually exclusive broader market classifications.
SELECT
    CAST("MatterEnforcementFY" AS BIGINT) AS matterenforcementfy,
    "MatterEnforcementDate" AS matterenforcementdate,
    CAST("MatterNumber" AS BIGINT) AS matternumber,
    "MatterName" AS mattername,
    "MatterIndustry" AS matterindustry,
    "Matterhyperlink" AS matterhyperlink,
    "Matter Enforcement Type" AS matter_enforcement_type
FROM "ftc-ftc-merger-enforcement-actions"
