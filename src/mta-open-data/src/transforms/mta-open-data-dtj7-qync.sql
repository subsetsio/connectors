-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "plaza",
    "collection_date",
    "day_of_week",
    "holiday",
    "class_1",
    "class_2",
    "class_3",
    "class_4",
    "class_5",
    "class_6",
    "class_7",
    "class_8",
    "class_9",
    "class_10",
    "class_11",
    "class_12",
    "class_13",
    "class_14",
    "class_15",
    "class_16",
    "class_17",
    "class_18",
    "class_19",
    "class_20",
    "class_21",
    "class_31",
    "class_32",
    "class_33",
    "class_34",
    "class_35",
    "class_36",
    "class_37",
    "class_38",
    "class_39",
    "total"
FROM "mta-open-data-dtj7-qync"
