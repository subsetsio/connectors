-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PURCHASE_COUNTRY: Country of purchase" AS purchase_country_country_of_purchase,
    "COICOP: Product category" AS coicop_product_category,
    "FREQ: Frequency" AS freq_frequency,
    "UNIT: Unit" AS unit_unit,
    "STATUS_ACT: Status" AS status_act_status,
    "AGE: Age" AS age_age,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_COICOP: Note" AS note_coicop_note,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-c1304"
