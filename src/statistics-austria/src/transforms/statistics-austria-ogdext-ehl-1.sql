-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "s_1311",
    "r091r154x",
    "c_421754b",
    "col" AS "statistics_austria_unit_id",
    "abbag_abbaumanagementgesellschaft_des_bundes",
    "col_2" AS "effective_date",
    "col_3" AS "sector_code_numeric",
    "bund",
    "col_4" AS "federal_state",
    "d",
    "col_5" AS "note"
FROM "statistics-austria-ogdext-ehl-1"
