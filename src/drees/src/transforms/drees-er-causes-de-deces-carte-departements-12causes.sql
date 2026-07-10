-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "column_1",
    "nom_dep",
    "num_dep",
    "covid_19",
    "causes_externes_de_morbidite_et_mortalite",
    "maladies_de_l_appareil_digestif",
    "maladies_de_l_appareil_genito_urinaire",
    "maladies_de_l_appareil_respiratoire",
    "maladies_du_systeme_nerveux_et_des_organes_des_sens",
    "maladies_endocriniennes_nutritionnelles_et_metaboliques",
    "maladies_infectieuses_et_parasitaires",
    "symptomes_et_etats_morbides_mal_definis",
    "toutes_causes",
    "troubles_mentaux_et_du_comportement",
    "tumeurs",
    "taux_trous_collecte",
    "geom",
    "centroid"
FROM "drees-er-causes-de-deces-carte-departements-12causes"
