-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Zone is a bidding-zone or country code and tech is the generation technology. Capacity factor, market value, and capture value are ratios or prices, not volumes; averaging them across zones without weighting by generation is misleading.
SELECT
    "zone",
    "year",
    "tech",
    "CF" AS cf,
    "MV" AS mv,
    "CV" AS cv,
    "composition"
FROM "bruegel-eu-renewables-value-tracker"
