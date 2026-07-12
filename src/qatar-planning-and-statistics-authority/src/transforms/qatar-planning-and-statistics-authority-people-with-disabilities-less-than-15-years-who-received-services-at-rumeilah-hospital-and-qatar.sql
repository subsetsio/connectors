-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_disability",
    "nw_l_q",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-people-with-disabilities-less-than-15-years-who-received-services-at-rumeilah-hospital-and-qatar"
