-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "male",
    "female",
    "not_designated",
    "trainingentity",
    "trainingsite",
    "borough",
    "adaptive_class",
    "starttime",
    "classname"
FROM "nyc-open-data-wnhd-n675"
