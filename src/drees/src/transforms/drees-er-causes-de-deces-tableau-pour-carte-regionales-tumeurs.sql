-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "column_1",
    "region",
    "code_reg",
    "tumeurs",
    "dont_autres_tumeurs_malignes",
    "dont_tumeur_maligne_de_la_prostate",
    "dont_tumeur_maligne_de_la_trachee_des_bronches_et_du_poumon",
    "dont_tumeur_maligne_de_la_vessie",
    "dont_tumeur_maligne_de_l_estomac",
    "dont_tumeur_maligne_de_l_osophage",
    "dont_tumeur_maligne_du_cerveau_et_du_systeme_nerveux_central",
    "dont_tumeur_maligne_du_colon_rectum_et_anus",
    "dont_tumeur_maligne_du_foie_et_des_voies_biliaires_intrahepatiques",
    "dont_tumeur_maligne_du_pancreas",
    "dont_tumeur_maligne_du_sein",
    "dont_tumeurs_malignes_de_la_levre_de_la_cavite_buccale_et_du_pharynx",
    "dont_tumeurs_non_malignes_benignes_et_incertaines",
    "geom",
    "centroid"
FROM "drees-er-causes-de-deces-tableau-pour-carte-regionales-tumeurs"
