-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ProvincialLevies" AS provinciallevies,
    "Regions" AS regions,
    "Periods" AS periods,
    "ProvincialLeviesInMillionOfEuros_1" AS provincialleviesinmillionofeuros_1,
    "ProvincialLevies_label" AS provinciallevies_label,
    "Regions_label" AS regions_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-7486eng"
