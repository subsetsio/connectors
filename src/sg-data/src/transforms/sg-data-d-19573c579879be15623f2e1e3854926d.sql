-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "company_name",
    "uen_no",
    "class",
    "class_code",
    "additional_info",
    "expiry_date",
    "building_no",
    "street_name",
    "unit_no",
    "building_name",
    "postal_code",
    "tel_no"
FROM "sg-data-d-19573c579879be15623f2e1e3854926d"
