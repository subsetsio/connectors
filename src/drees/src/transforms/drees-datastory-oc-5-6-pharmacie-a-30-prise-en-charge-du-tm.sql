-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "familles_d_organismes",
    "type_d_organismes",
    "en_" AS en,
    CAST("annee" AS BIGINT) AS annee,
    "prise_en_charge_ticket_moderateur"
FROM "drees-datastory-oc-5-6-pharmacie-a-30-prise-en-charge-du-tm"
