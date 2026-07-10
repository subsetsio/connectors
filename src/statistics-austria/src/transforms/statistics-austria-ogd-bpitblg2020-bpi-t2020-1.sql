-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "branch_of_civil_engineering",
    "total",
    "preliminary_excavation_und_earthworks_group_06",
    "drainage_and_cable_trench_work_group_08",
    "pipes_gutters_sewage_disposal_and_drainage_by_gravity_group_10",
    "shafts_and_coverings_group_12",
    "concrete_and_reinforced_concrete_work_and_masonry_group_31",
    "subgrade_level_unbound_base_course_group_25",
    "bituminous_roadbases_and_wearing_courses_group_26",
    "concrete_floor_cement_stabilized_base_courses_group_28",
    "plasterworks_and_margins_group_29",
    "noise_protection_facilities_group_42",
    "road_equipment_group_43",
    "preliminary_excavation_and_earthworks_group_06",
    "foundation_work_group_19",
    "concrete_and_reinforced_concrete_work_and_masonry_group_31_2",
    "surface_protection_sealing_of_concrete_group_32",
    "steel_construction_group_35",
    "bridge_equipment_group_41",
    "subgrade_level_unbound_base_courses_group_25",
    "bituminous_roadbases_and_wearing_courses_group_26_2",
    "drainage_and_cable_trench_work_group_08_2",
    "concrete_and_reinforced_concrete_work_and_masonry_group_31_3",
    "subgrade_level_unbound_base_courses_group_25_2",
    "bituminous_roadbases_and_wearing_courses_group_26_3",
    "pipes_gutters_sewage_disposal_and_drainage_by_gravity_group_10_2",
    "pipes_water_supply_and_pressure_line_group_09",
    "shafts_and_coverings_group_12_2",
    "underground_new_installation_group_15"
FROM "statistics-austria-ogd-bpitblg2020-bpi-t2020-1"
