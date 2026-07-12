-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PRODUCT: Product" AS product_product,
    "SPECIFICATION: Specification" AS specification_specification,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_PRODUCT_2: Note Product 2" AS note_product_2_note_product_2,
    "NOTE_PRODUCT_1: Note Product 1" AS note_product_1_note_product_1,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-a4304"
