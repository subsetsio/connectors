-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "reporting_month",
    "value_and_volume_selection",
    "oe_cpa_2_digit",
    "sold_production_s",
    "technical_total_production_tt",
    "total_production_t",
    "economic_total_production_et"
FROM "statistics-austria-ogd-prodcom002-prodcom-mo-1"
