-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "district",
    "school_name",
    "is_org_splitsited",
    "building_ids",
    "transfer_school",
    "_201415" AS 201415,
    "_201415_1" AS 201415_1,
    "_201415_2" AS 201415_2,
    "_201415_3" AS 201415_3,
    "_201415_4" AS 201415_4,
    "_201415_5" AS 201415_5,
    "_201415_6" AS 201415_6,
    "_201415_7" AS 201415_7,
    "_201415_8" AS 201415_8,
    "_201415_9" AS 201415_9,
    "_201415_10" AS 201415_10,
    "_201415_11" AS 201415_11,
    "_201415_12" AS 201415_12,
    "_201415_13" AS 201415_13,
    "_201415_14" AS 201415_14,
    "_201415_15" AS 201415_15,
    "_201415_16" AS 201415_16,
    "_201314" AS 201314,
    "_201314_1" AS 201314_1,
    "_201314_2" AS 201314_2
FROM "nyc-open-data-g4zf-s85y"
