-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Mixes aggregate rows (maturite/modalite null) with detailed breakdown rows; filter to one level before aggregating.
SELECT
    "serie_id",
    "serie_label",
    "age",
    "prestation",
    "annee",
    "maturite",
    "maturite_a_privilegier",
    "modalite",
    "unite",
    "valeur",
    "statut_diffusion"
FROM "drees-trajectoires-des-beneficiaires-de-minima-sociaux"
