-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains per-country component scores by underlying CPI source for the latest CPI edition, so aggregate only after accounting for source_name.
SELECT
    "country",
    "iso3",
    "region",
    "source_name",
    "source_score"
FROM "transparency-international-cpi-latest-detail"
