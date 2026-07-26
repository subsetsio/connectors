-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "boroughcitywide_office_bco",
    "district",
    "school",
    "school_name",
    "school_category",
    "_program" AS program,
    "_language" AS language,
    "language_translated",
    "generalspecial_education",
    "special_education_model"
FROM "nyc-open-data-rrd7-vuvp"
