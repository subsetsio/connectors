-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Historical civil penalty actions file is frozen; use the fiscal year and enforcement date columns as source-reported enforcement timing.
SELECT
    CAST("MatterEnforcementFY" AS BIGINT) AS matterenforcementfy,
    "MatterEnforcementDate" AS matterenforcementdate,
    "MatterName" AS mattername,
    CAST("MatterNumber" AS BIGINT) AS matternumber,
    "MatterEnforcementType" AS matterenforcementtype,
    "Matterhyperlink" AS matterhyperlink,
    "MatterType" AS mattertype
FROM "ftc-ftc-civil-penalty-actions"
