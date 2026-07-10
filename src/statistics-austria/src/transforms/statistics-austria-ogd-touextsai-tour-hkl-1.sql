-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "season_tourism_month",
    "bundesland",
    "country_of_origin",
    "arrivals",
    "nights_spent"
FROM "statistics-austria-ogd-touextsai-tour-hkl-1"
