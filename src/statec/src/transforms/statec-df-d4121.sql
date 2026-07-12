-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "REF_AREA: Reference area" AS ref_area_reference_area,
    "CANTON: Canton" AS canton_canton,
    "REGION: Region" AS region_region,
    "FREQ: Frequency" AS freq_frequency,
    "PRODUCT_BCS: Building type" AS product_bcs_building_type,
    "INDICATOR_BCS: BCS Indicator" AS indicator_bcs_bcs_indicator,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "CONF_STATUS: Confidentiality status" AS conf_status_confidentiality_status,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "UNIT_MEASURE: Measure unit" AS unit_measure_measure_unit,
    "DECIMALS: Decimal" AS decimals_decimal
FROM "statec-df-d4121"
