-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Every measure ships twice: a French-formatted VARCHAR and a parsed `*_integer` numeric of the same quantity.
-- caution: The `*_moyens` columns are per-practitioner means and the `taux_depassement*` columns are percentages — neither is summable. The territory columns mix département, région and national rows.
SELECT
    "annee",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "hono_sans_depassement_totaux",
    "depassements_totaux",
    "hono_sans_depassement_moyens",
    "depassements_moyens",
    "taux_depassement_s2",
    "taux_depassement_s2_non_optam",
    "taux_depassement_s2_optam",
    "vision_generale_all",
    "vision_generale_prescriptions",
    "vision_profession_territoire",
    "taux_depassement",
    "hono_sans_depassement_totaux_integer",
    "depassements_totaux_integer",
    "hono_sans_depassement_moyens_integer",
    "depassements_moyens_integer",
    "taux_depassement_s2_integer",
    "taux_depassement_s2_non_optam_integer",
    "taux_depassement_s2_optam_integer",
    "totaux_integer",
    "moyens_integer"
FROM "cnam-honoraires"
