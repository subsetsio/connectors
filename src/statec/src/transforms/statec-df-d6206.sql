-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "SPECIFICATION: Specification" AS specification_specification,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_SPEC2: Note specification" AS note_spec2_note_specification,
    "NOTE_SPEC1: Note specification" AS note_spec1_note_specification,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d6206"
