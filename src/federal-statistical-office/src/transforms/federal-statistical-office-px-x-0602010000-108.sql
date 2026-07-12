-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("jahr" AS BIGINT) AS jahr,
    "kanton",
    "wirtschaftssektor",
    "öffentlicher_privater_sektor" AS ffentlicher_privater_sektor,
    "wirtschaftliche_ausrichtung",
    "beobachtungseinheit",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0602010000-108"
