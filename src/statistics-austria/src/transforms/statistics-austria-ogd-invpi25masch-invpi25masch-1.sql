-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "c_28_machinery_and_equipment",
    "c_281_general_purpose_machinery",
    "c_282_other_general_purpose_machinery",
    "c_283_agricultural_and_forestry_machinery",
    "c_284_metal_forming_machinery_and_machine_tools",
    "c_289_other_special_purpose_machinery"
FROM "statistics-austria-ogd-invpi25masch-invpi25masch-1"
