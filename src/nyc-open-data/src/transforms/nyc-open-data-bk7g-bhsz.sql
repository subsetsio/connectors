-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_title",
    "identifier",
    "_level" AS level,
    "date",
    "instances_container",
    "instances_container_profile",
    "instances_instances_digital_object",
    "instances_instances_instance_type",
    "instances_instances_is_representative",
    "instances_instances_container_2",
    "instances_instances_container_3"
FROM "nyc-open-data-bk7g-bhsz"
