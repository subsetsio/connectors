-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "SIZECLAS: Size class" AS sizeclas_size_class,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "LEG_FORM: Legal form" AS leg_form_legal_form,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels
FROM "statec-dsd-demo-ent-2@df-d1307"
