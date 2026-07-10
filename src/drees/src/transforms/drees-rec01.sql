-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champs",
    "annee",
    "sexe",
    "variable",
    "intitule",
    "auvergne_rhone_alpes",
    "bourgogne_franche_comte",
    "bretagne",
    "centre_val_de_loire",
    "corse",
    "grand_est",
    "hauts_de_france",
    "ile_de_france",
    "normandie",
    "nouvelle_aquitaine",
    "occitanie",
    "pays_de_la_loire",
    "provence_alpes_cote_d_azur",
    "drom",
    "ensemble"
FROM "drees-rec01"
