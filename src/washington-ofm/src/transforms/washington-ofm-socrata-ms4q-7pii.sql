-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    CAST("age" AS BIGINT) AS age,
    "age5",
    "age0_2",
    "age_0_17",
    "agev",
    CAST("age5sort" AS BIGINT) AS age5sort,
    "age5_17",
    "age12_17",
    "age17_22",
    "age17_29",
    "age18_39",
    "age18_54",
    "age18_64",
    "age20_64",
    "age65",
    "age70",
    "age75",
    "age80",
    "age85"
FROM "washington-ofm-socrata-ms4q-7pii"
