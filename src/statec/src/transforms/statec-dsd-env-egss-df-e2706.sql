-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "CEP: Classification of Environmental Purposes (CEP)" AS cep_classification_of_environmental_purposes_cep,
    "TRANSACTION: Transaction" AS transaction_transaction,
    "PRICE_BASE: Price base" AS price_base_price_base,
    "ENV_ECON: Environmental economic characteristics" AS env_econ_environmental_economic_characteristics,
    "SECTOR: Sector" AS sector_sector,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_TS: Detailed description of the group of series" AS comment_ts_detailed_description_of_the_group_of_series
FROM "statec-dsd-env-egss@df-e2706"
