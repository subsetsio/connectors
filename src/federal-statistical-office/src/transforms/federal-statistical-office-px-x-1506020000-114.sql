-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("jahr" AS BIGINT) AS jahr,
    "form_des_ausbildungsbeitrags",
    "kanton",
    "bildungsstufe",
    "betrag_und_bezügerinnen_und_bezüger" AS betrag_und_bez_gerinnen_und_bez_ger,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1506020000-114"
