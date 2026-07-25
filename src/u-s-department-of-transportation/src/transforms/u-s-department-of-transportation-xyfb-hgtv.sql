-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("quarter" AS BIGINT) AS quarter,
    "mkt_carrier",
    CAST("mkt_carrier_airline_id" AS BIGINT) AS mkt_carrier_airline_id,
    "mkt_carrier_name",
    "mkt_unique_carrier",
    "mkt_unique_carrier_name",
    "op_carrier",
    CAST("op_carrier_airline_id" AS BIGINT) AS op_carrier_airline_id,
    "op_carrier_name",
    "op_unique_carrier",
    "op_unique_carrier_name",
    CAST("pax_alt_trans" AS BIGINT) AS pax_alt_trans,
    CAST("pax_no_alt_trans" AS BIGINT) AS pax_no_alt_trans,
    CAST("pax_no_comp_1" AS BIGINT) AS pax_no_comp_1,
    CAST("pax_no_comp_2" AS BIGINT) AS pax_no_comp_2,
    CAST("pax_no_comp_3" AS BIGINT) AS pax_no_comp_3,
    CAST("tot_den_boarding" AS BIGINT) AS tot_den_boarding,
    CAST("pax_comp_1" AS BIGINT) AS pax_comp_1,
    CAST("pax_comp_2" AS BIGINT) AS pax_comp_2,
    CAST("pax_upgrade" AS BIGINT) AS pax_upgrade,
    CAST("pax_downgrade" AS BIGINT) AS pax_downgrade,
    CAST("tot_boarding" AS BIGINT) AS tot_boarding,
    CAST("comp_paid_1" AS BIGINT) AS comp_paid_1,
    CAST("comp_paid_2" AS BIGINT) AS comp_paid_2,
    CAST("comp_paid_3" AS BIGINT) AS comp_paid_3,
    CAST("code_share" AS BOOLEAN) AS code_share,
    "op_carrier_source"
FROM "u-s-department-of-transportation-xyfb-hgtv"
