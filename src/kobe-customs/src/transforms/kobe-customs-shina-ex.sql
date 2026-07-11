-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This port-by-commodity export matrix includes commodity totals, composition shares, year-on-year rates, and contribution measures alongside trade values, so filter to the intended measure before aggregating values.
SELECT
    "year",
    "classification",
    "sheet",
    "row_label",
    "col_header",
    "row_idx",
    "col_idx",
    "value"
FROM "kobe-customs-shina-ex"
