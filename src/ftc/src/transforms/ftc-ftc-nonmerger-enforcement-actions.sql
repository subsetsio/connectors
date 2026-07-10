-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are FTC nonmerger enforcement matters; the upstream CSV contains at least one exact duplicate row, and industry is a source category rather than a complete industry taxonomy.
SELECT
    CAST("MatterEnforcementFY" AS BIGINT) AS matterenforcementfy,
    "MatterEnforcementDate" AS matterenforcementdate,
    CAST("MatterNumber" AS BIGINT) AS matternumber,
    "MatterName" AS mattername,
    "MatterEnforcementType" AS matterenforcementtype,
    "MatterIndustry" AS matterindustry,
    "Matterhyperlink" AS matterhyperlink
FROM "ftc-ftc-nonmerger-enforcement-actions"
