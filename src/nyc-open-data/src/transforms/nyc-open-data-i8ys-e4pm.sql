-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boro",
    "csd",
    "school_code",
    "school_name",
    "grade",
    "program_type",
    "core_subject912_only",
    "core_course912_only",
    "service_categoryk9_only",
    "number_of_classes",
    "total_registeras_of_12308",
    "average_class_size",
    "size_of_smallest_classas_of_12308",
    "size_of_largest_classas_of_12308"
FROM "nyc-open-data-i8ys-e4pm"
