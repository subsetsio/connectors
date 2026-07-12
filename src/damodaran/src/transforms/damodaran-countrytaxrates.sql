-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source contains repeated country and tax-rate labels, including exact duplicate rows in the normalized raw table; aggregate only after deduplicating or selecting the intended row set.
SELECT
    "region",
    "category",
    "metric",
    "value"
FROM "damodaran-countrytaxrates"
