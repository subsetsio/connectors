-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the measure-definition catalog only; it does not contain monthly measure observations by organisation.
SELECT
    "measure_id",
    "name",
    "title",
    "description",
    "why_it_matters",
    "tags",
    "numerator_short",
    "denominator_short",
    "is_percentage",
    "is_cost_based",
    "low_is_good",
    "numerator_type",
    "denominator_type",
    "measure_type",
    "measure_complexity",
    "date_reviewed"
FROM "openprescribing-measures"
