-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "latitude",
    "longitude",
    "initial_imsr_date",
    "fire_name",
    "incident_id",
    "x100pct",
    "imt_type",
    "gacc",
    "new_to_imsr",
    "post_date_isoformat",
    "IrwinID" AS irwinid,
    "IrwinFireDiscoveryDateTime" AS irwinfirediscoverydatetime,
    "IsLatest" AS islatest,
    "Occurrence" AS occurrence,
    "size",
    "UniqueFireIdentifier" AS uniquefireidentifier,
    "nmbr_apprs",
    "intl_imsr_post_date"
FROM "nifc-85d3f50b5eee4dcfa48f5e4fb23aa9e1-0"
