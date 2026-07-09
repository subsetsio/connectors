-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Commodity includes the total ALL alongside components, partner includes aggregates and inconsistent country labels from the source sheet headers, and unit includes spelling variants for the same unit. Values are only comparable within one unit and seasonal_adj combination.
SELECT
    "date",
    "commodity",
    "unit",
    "seasonal_adj",
    "flow",
    "partner",
    "value"
FROM "bruegel-global-trade-tracker"
