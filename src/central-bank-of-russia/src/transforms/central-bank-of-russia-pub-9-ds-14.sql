-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are source-provided long-format observations; measure and series labels are Bank of Russia header dimensions and differ by dataset. Filter the relevant measure, series, and unit before aggregating values.
SELECT
    "publication_id",
    "dataset_id",
    "date",
    "period_label",
    "periodicity",
    "measure_id",
    "measure_name",
    "element_id",
    "element_name",
    "unit_id",
    "unit",
    "obs_val"
FROM "central-bank-of-russia-pub-9-ds-14"
