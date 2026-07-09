-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `year` is a fiscal academic year (e.g. '2020-21').
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "indicator",
    "year",
    "state",
    "value",
    "gender",
    "education_level",
    "social_category",
    "social_group",
    "learning_mode",
    "institution_type",
    "faculty_type"
FROM "mospi-aishe-getaisherecords"
