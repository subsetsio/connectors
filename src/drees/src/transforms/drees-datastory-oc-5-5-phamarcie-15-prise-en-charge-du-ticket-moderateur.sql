-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "familles_d_organismes",
    "type_de_contrats",
    "en_" AS en,
    CAST("annee" AS BIGINT) AS annee,
    "prise_en_charge_du_ticket_moderateur"
FROM "drees-datastory-oc-5-5-phamarcie-15-prise-en-charge-du-ticket-moderateur"
