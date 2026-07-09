-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Seventeen directed classification pairs are stacked in one table; filter BOTH `source_classification` and `target_classification` before joining, or a code is converted through every revision at once.
-- caution: `weight` apportions a source code across its target codes and sums to 1 within a (source_classification, target_classification, source_code) group — multiply values by `weight` when converting, never sum the rows.
SELECT
    "source_classification",
    "source_code",
    "target_classification",
    "target_code",
    "weight"
FROM "harvard-growth-lab-atlas-of-economic-complexity-weighted-classification-conversion-tables"
