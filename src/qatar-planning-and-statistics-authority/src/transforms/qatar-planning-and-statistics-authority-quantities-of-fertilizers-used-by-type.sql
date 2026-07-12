-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nw_lsmd",
    "type_of_fertilizer",
    "value_ton"
FROM "qatar-planning-and-statistics-authority-quantities-of-fertilizers-used-by-type"
