-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are survey observations for Duffy phenotype data and should not be interpreted as administrative-area totals.
SELECT
    "gid",
    CAST("id" AS BIGINT) AS id,
    "country",
    "latitude",
    "longitude",
    "area_type",
    CAST("no_examine" AS BIGINT) AS no_examine,
    "diagnostic",
    CAST("prom_posit" AS BIGINT) AS prom_posit,
    CAST("prom_negat" AS BIGINT) AS prom_negat,
    CAST("phe_no_a_b" AS BIGINT) AS phe_no_a_b,
    CAST("phe_no_a_1" AS BIGINT) AS phe_no_a_1,
    CAST("phe_no_a_2" AS BIGINT) AS phe_no_a_2,
    CAST("phe_no_a_3" AS BIGINT) AS phe_no_a_3,
    CAST("aphe_no_a_" AS BIGINT) AS aphe_no_a,
    CAST("aphe_no_a1" AS BIGINT) AS aphe_no_a1,
    CAST("bphe_no_b_" AS BIGINT) AS bphe_no_b,
    CAST("bphe_no_b1" AS BIGINT) AS bphe_no_b1,
    CAST("genfyafya" AS BIGINT) AS genfyafya,
    CAST("fya_fyb" AS BIGINT) AS fya_fyb,
    CAST("fyb_fyb" AS BIGINT) AS fyb_fyb,
    CAST("fybesfybes" AS BIGINT) AS fybesfybes,
    CAST("fya_fybes" AS BIGINT) AS fya_fybes,
    CAST("fyb_fybes" AS BIGINT) AS fyb_fybes,
    CAST("fya_fyaes" AS BIGINT) AS fya_fyaes,
    CAST("fyb_fyaes" AS BIGINT) AS fyb_fyaes,
    CAST("fybesfyaes" AS BIGINT) AS fybesfyaes,
    CAST("fyaesfyaes" AS BIGINT) AS fyaesfyaes,
    "citation",
    "country_id",
    "malaria_metrics_available",
    "_source_type_name" AS source_type_name,
    "_feature_id" AS feature_id,
    "_geometry_name" AS geometry_name,
    "_geometry" AS geometry,
    "_bbox" AS bbox
FROM "malaria-atlas-project-explorer:duffy-data"
