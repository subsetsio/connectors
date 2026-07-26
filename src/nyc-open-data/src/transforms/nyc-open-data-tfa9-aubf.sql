-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "school_type",
    "final_202122_number_of_classes",
    "final_202122_number_of_students",
    "final_202122_average_class_size",
    "final_201920_number_of_classes",
    "final_201920_number_of_students",
    "final_201920_average_class_size",
    "diff_number_of_classes",
    "diff_number_of_students",
    "diff_average_class_size"
FROM "nyc-open-data-tfa9-aubf"
