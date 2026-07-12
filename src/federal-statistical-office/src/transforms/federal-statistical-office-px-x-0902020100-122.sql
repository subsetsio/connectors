-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kanton",
    "gebäudekategorie" AS geb_udekategorie,
    "bauperiode",
    "heizungsart",
    "energieträger_der_heizung" AS energietr_ger_der_heizung,
    "warmwasserversorgung",
    "energieträger_für_warmwasser" AS energietr_ger_f_r_warmwasser,
    CAST("jahr" AS BIGINT) AS jahr,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0902020100-122"
