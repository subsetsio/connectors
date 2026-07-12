-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "activites_et_services",
    "libelle_technique",
    "definition"
FROM "urssaf-lexique-des-activites-et-des-services-de-lurssaf"
