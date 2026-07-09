-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Category is the measurement basis, not a grouping label: Divisia index rows and simple-sum euro rows are not comparable. Subcategory selects the euro-area composition, so the same date and series_name appears several times.
SELECT
    "date",
    "series_name",
    "category",
    "subcategory",
    "value"
FROM "bruegel-divisia-monetary-aggregates-euro-area"
