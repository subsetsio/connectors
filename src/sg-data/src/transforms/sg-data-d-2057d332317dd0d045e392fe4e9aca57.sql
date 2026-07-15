-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "property_location",
    "mode_of_allocation",
    "land_area",
    "gross_floor_area",
    "tendered_uses",
    "tenure",
    "closing_date",
    "award_date",
    "awarded_usage",
    "award_value_per_month_for_the_first_term_tenancy",
    "successful_bidder"
FROM "sg-data-d-2057d332317dd0d045e392fe4e9aca57"
