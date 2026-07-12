-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "stadt_agglomeration",
    "indikator_zur_persönlichen_sicherheit" AS indikator_zur_pers_nlichen_sicherheit,
    "absolut_relativ",
    CAST("jahr" AS BIGINT) AS jahr,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-2105000000-207"
