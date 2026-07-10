-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Crosswalk rows are vintage-specific ZIP-to-HSA/HRR assignments; include `vintage` when comparing or joining across years.
SELECT
    "zipcode",
    "hsa_num",
    "hsa_city",
    "hsa_state",
    "hrr_num",
    "hrr_city",
    "hrr_state",
    "vintage"
FROM "dartmouth-atlas-of-health-care-geography-crosswalk"
