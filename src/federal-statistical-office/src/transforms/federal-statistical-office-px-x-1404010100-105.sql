-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kosten_und_erlöse" AS kosten_und_erl_se,
    "betriebstyp",
    "leistungstyp",
    "aktivität" AS aktivit_t,
    "garant",
    CAST("jahr" AS BIGINT) AS jahr,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1404010100-105"
