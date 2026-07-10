-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Mixes overall rows with partition/subgroup breakdown rows (varpartition/vargroupage null on the overall rows); select a single breakdown level before aggregating.
SELECT
    "type",
    "vartaux",
    "vartauxlib",
    "i_cat",
    "cat",
    "catlib",
    "varpartition",
    "valpartition",
    "vargroupage",
    "valgroupage",
    "varpoids",
    "poids1",
    "poidstot",
    "txnonstand",
    "txstanddir",
    "txstanddirmodbb",
    "txstanddirmodbh",
    "txstandindir",
    "txstandindirmodbb",
    "txstandindirmodbh"
FROM "drees-er-inegalites-maladies-chroniques"
