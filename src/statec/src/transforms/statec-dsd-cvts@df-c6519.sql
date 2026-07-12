-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE: Measure" AS measure_measure,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "FREQ: Frequency" AS freq_frequency,
    "SIZECLAS: Size class" AS sizeclas_size_class,
    "TRAINING: Training" AS training_training,
    "SEX: Sex" AS sex_sex,
    "COST: Costs" AS cost_costs,
    "SKILL: Skill" AS skill_skill,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "TIME_PERIOD: Time Period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-dsd-cvts@df-c6519"
