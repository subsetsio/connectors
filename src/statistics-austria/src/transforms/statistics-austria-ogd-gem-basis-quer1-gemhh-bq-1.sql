-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "commune_2413",
    "number_of_communes",
    "ordinary_expenditures_in_total",
    "ordinary_revenuess_in_total",
    "extraordinary_expenditures_in_total",
    "extraordinary_revenues_in_total",
    "municipal_rates_in_total",
    "charges",
    "profit_shares",
    "casino_tax",
    "inhabitants",
    "debts_final_result_in_total"
FROM "statistics-austria-ogd-gem-basis-quer1-gemhh-bq-1"
