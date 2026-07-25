-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "TYPE_FAM_NUC: Type of family nucleus" AS type_fam_nuc_type_of_family_nucleus,
    "SIZE_FAM_NUC: Size of family nucleus" AS size_fam_nuc_size_of_family_nucleus,
    "TYPE_PRV_HH: Type of household" AS type_prv_hh_type_of_household,
    "SIZE_PRV_HH: Size of household" AS size_prv_hh_size_of_household,
    "TENURE_STATUS_HH: Tenure status of household" AS tenure_status_hh_tenure_status_of_household,
    "TYPE_LIVE_QUARTER: Type of living quarter" AS type_live_quarter_type_of_living_quarter,
    "OCC_STATUS_CONV: Occupancy status" AS occ_status_conv_occupancy_status,
    "TYPE_OWN: Type of ownership" AS type_own_type_of_ownership,
    "OCC_NB: Number of occupants" AS occ_nb_number_of_occupants,
    "FLOOR_USE: Useful floor space" AS floor_use_useful_floor_space,
    "ROOM_NB: Number of rooms" AS room_nb_number_of_rooms,
    "DENSITY_STD: Density standard (floor space)" AS density_std_density_standard_floor_space,
    "TYPE_BUILD_DWE: Type of building" AS type_build_dwe_type_of_building,
    "CONSTR_PERIOD_DWE: Construction period" AS constr_period_dwe_construction_period,
    "GEO: Geographic level" AS geo_geographic_level,
    "ROOM_NB_OCC: Number of rooms per occupant" AS room_nb_occ_number_of_rooms_per_occupant,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-dsd-census-nb-log-cla@df-b1707"
