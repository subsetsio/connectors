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
    "_201516" AS 201516,
    "_201516_1" AS 201516_1,
    "_201516_2" AS 201516_2,
    "_201516_3" AS 201516_3,
    "_201516_4" AS 201516_4,
    "_201516_5" AS 201516_5,
    "_201516_6" AS 201516_6,
    "_201516_7" AS 201516_7,
    "_201516_8" AS 201516_8,
    "_201516_9" AS 201516_9,
    "_201516_10" AS 201516_10,
    "_201516_11" AS 201516_11,
    "_201516_12" AS 201516_12,
    "_201516_13" AS 201516_13,
    "_201516_14" AS 201516_14,
    "_201516_15" AS 201516_15,
    "_201516_16" AS 201516_16,
    "_201516_17" AS 201516_17,
    "_201415" AS 201415,
    "_201415_1" AS 201415_1,
    "_201415_2" AS 201415_2
FROM "nyc-open-data-herb-qubg"
