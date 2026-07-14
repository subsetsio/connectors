-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are directional country pairs even when many language proximity measures are symmetric.
SELECT
    "iso_o",
    "country_o",
    "iso_d",
    "country_d",
    "col",
    "csl",
    "cnl",
    "prox1",
    "lp1",
    "prox2",
    "lp2",
    "cl",
    "cle"
FROM "cepii-language"
