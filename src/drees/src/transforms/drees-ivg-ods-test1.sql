-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zone_geographique",
    "annee",
    "ivg_en_etablissements_hospitaliers_methode_instrumentale",
    "ivg_en_etablissements_hospitaliers_methode_medicamenteuse",
    "ivg_en_etablissements_hospitaliers_methode_non_precisee",
    "ivg_hors_etablissements_hospitaliers_cabinet_liberal",
    "ivg_hors_etablissements_hospitaliers_centres",
    "total_ivg",
    "taux_de_recours_p_1000_femmes_de_15_a_49_ans",
    "ivg_en_etablissements_hospitaliers",
    "ivg_hors_etablissements_hospitaliers",
    "dep_code",
    "reg_name",
    "reg_code",
    "geo_shape",
    "geo_point_2d"
FROM "drees-ivg-ods-test1"
