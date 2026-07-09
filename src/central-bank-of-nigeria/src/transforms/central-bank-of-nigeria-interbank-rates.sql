-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: (`ratedate`, `ratetype`) is NOT unique: 46 date/rate-type pairs carry more than one row, most of them divergent restatements. Deduplicate before building a per-rate-type daily series.
-- caution: The `ratetype` domain is not clean: `OBB` appears once alongside the 4,375 rows labelled `OBB Rate`, and the tenor labels mix two conventions (`7-Day`/`30-Day`/`360-Day` against the one-off `4-7 Days` and `8-35 Days` buckets). Group on a normalised rate type, not the raw string.
-- caution: `range` is a free-text low-high pair (e.g. `22.0000-24.0000`), sometimes padded with spaces — it is a string, not two numbers.
-- caution: Rates are percent per annum and the rate types are different instruments (overnight open-buy-back, call, and term placements), so rows from different `ratetype` values must not be averaged together.
SELECT
    "id",
    "ratedate",
    "ratetype",
    "range",
    "weightedaverage"
FROM "central-bank-of-nigeria-interbank-rates"
