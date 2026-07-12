-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "libelle_zone_d_emploi",
    "zone_d_emploi",
    "region",
    "ancienne_region",
    "libelle_zone_d_emploi_reg",
    "zone_d_emploi_regionalisee",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "code_region",
    "code_ancienne_region",
    "code_zone_d_emploi",
    "code_zone_d_emploi_regionalisee",
    "effectifs_salaries_brut",
    "effectifs_salaries_cvs",
    "masse_salariale_brut",
    "masse_salariale_cvs"
FROM "urssaf-effectifs-salaries-et-masse-salariale-du-secteur-prive-par-zone-demploi"
