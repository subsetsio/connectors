-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fire_name",
    "post_date_isoformat",
    "OBJECTID" AS objectid,
    "latitude",
    "longitude",
    "initial_imsr_date",
    "incident_id",
    "size",
    "x100pct",
    "imt_type",
    "new_to_imsr",
    "gacc",
    "GACC_20250113" AS gacc_20250113,
    "IrwinID" AS irwinid,
    "IrwinFireDiscoveryDateTime" AS irwinfirediscoverydatetime,
    "UniqueFireIdentifier" AS uniquefireidentifier,
    "Occurrence" AS occurrence,
    CAST("post_year" AS BIGINT) AS post_year,
    "post_month",
    strptime("post_date_textformat", '%Y%m%d')::DATE AS post_date_textformat,
    "intl_imsr_post_date",
    "nmbr_apprs"
FROM "nifc-eaa333df1850483abdd0465f86212e03-0"
