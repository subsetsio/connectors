-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ndeg_depot_ndeg_enregistrement",
    "date_de_depot",
    "date_d_enregistrement",
    "date_d_expiration",
    "territoire",
    "classes",
    "marque"
FROM "urssaf-marques-deposees-acoss-urssaf"
