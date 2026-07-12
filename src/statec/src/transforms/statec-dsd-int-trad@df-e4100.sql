-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "BASE_PERIOD: Base period" AS base_period_base_period,
    "C_PART: Partner country" AS c_part_partner_country,
    "C_IMP: Country of origin" AS c_imp_country_of_origin,
    "C_EXP: Country of destination" AS c_exp_country_of_destination,
    "SITC06: Trade classification (SITC, 2006)" AS sitc06_trade_classification_sitc_2006,
    "BEC_R4: Broad economic categories (BEC Rev.4)" AS bec_r4_broad_economic_categories_bec_rev_4,
    "RANK: Rank" AS rank_rank,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-dsd-int-trad@df-e4100"
