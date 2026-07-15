-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year_PlacementType_Total" AS year_placementtype_total
FROM "sg-data-d-b85f15701092578c2aa0ae8cd263b210"
