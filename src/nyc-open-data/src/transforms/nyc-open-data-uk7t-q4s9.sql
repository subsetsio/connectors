-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "location_category_description",
    "_1819_complaints_julydecember" AS 1819_complaints_julydecember,
    "_1819_material_incidents_julydecember" AS 1819_material_incidents_julydecember,
    "_1819_disability_julydecember" AS 1819_disability_julydecember,
    "_1819_ethnicity_julydecember" AS 1819_ethnicity_julydecember,
    "_1819_gender_identityexpression_julydecember" AS 1819_gender_identityexpression_julydecember,
    "_1819_race_julydecember" AS 1819_race_julydecember,
    "_1819_religion_julydecember" AS 1819_religion_julydecember,
    "_1819_sex_julydecember" AS 1819_sex_julydecember,
    "_1819_sexual_orientation_julydecember" AS 1819_sexual_orientation_julydecember,
    "_1819_weight_julydecember" AS 1819_weight_julydecember,
    "_1819_total_bias_julydecember" AS 1819_total_bias_julydecember
FROM "nyc-open-data-uk7t-q4s9"
