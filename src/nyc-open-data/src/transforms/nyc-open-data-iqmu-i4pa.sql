-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "grade_level",
    "program_type",
    "number_of_students",
    "number_of_classes",
    "average_class_size",
    "minimum_class_size",
    "maximum_class_size"
FROM "nyc-open-data-iqmu-i4pa"
