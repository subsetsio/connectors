-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series",
    "main_aggregates_of_national_accounts",
    "nominal_seasonally_and_working_day_unadjusted_in_million_eur",
    "nominal_seasonally_and_working_day_adjusted_in_million_eur",
    "real_seasonally_and_working_day_unadjusted_in_million_eur",
    "real_seasonally_and_working_day_adjusted_in_million_eur"
FROM "statistics-austria-ogd-vgr108-vgr-ha-vj-1"
