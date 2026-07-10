-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series_annual_data",
    "general_government_4",
    "government_debt_total_101_in_mio_eur",
    "af_2_currency_and_deposits_102_in_mio_eur",
    "af_3_debt_securities_103_in_mio_eur",
    "af_4_loans_104_in_mio_eur"
FROM "statistics-austria-ogd-kons-brv-q-hvd-kons-brv-q-1"
