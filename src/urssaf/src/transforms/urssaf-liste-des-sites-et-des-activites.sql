-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "libelle_organisme",
    "code_site_v2",
    "code_organisme_ur_regionale",
    "identifiant_site_rioss",
    "libelle_site",
    "type_implantation",
    CAST("siege_social" AS BIGINT) AS siege_social,
    "adresse",
    "code_postal",
    "ville",
    "pays",
    CAST("latitude_du_site" AS DOUBLE) AS latitude_du_site,
    CAST("longitude_du_site" AS DOUBLE) AS longitude_du_site,
    "services",
    "activites_de_gestion_interne",
    "code_ancienne_region",
    "ancienne_region",
    "code_nouvelle_region",
    "nouvelle_region"
FROM "urssaf-liste-des-sites-et-des-activites"
