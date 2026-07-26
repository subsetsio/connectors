-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "district",
    "dbn",
    "schoolfood_code",
    "breakfast_before_bell_adp",
    "breakfast_after_bell_adp",
    "breakfast_before_bell",
    "breakfast_after_bell",
    "grab_go",
    "lunches_adp",
    "salad_bars",
    "snacks_adp",
    "suppers_adp"
FROM "nyc-open-data-h8ar-pcmr"
