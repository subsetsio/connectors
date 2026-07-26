-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "location_category_description",
    "complaints",
    "material_incidents",
    "race",
    "ethnicitynational_origin",
    "religion",
    "weight",
    "disability",
    "genderidentityexpression",
    "sex",
    "sexual_orientation",
    "unnamed_column",
    "bullying_har"
FROM "nyc-open-data-8h5p-ccrz"
