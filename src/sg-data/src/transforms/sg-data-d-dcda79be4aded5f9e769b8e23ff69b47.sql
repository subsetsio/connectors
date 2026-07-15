-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "company_name",
    "uen_no",
    "workhead",
    "grade",
    "additional_info",
    "expiry_date",
    "building_no",
    "street_name",
    "unit_no",
    "building_name",
    "postal_code",
    "tel_no"
FROM "sg-data-d-dcda79be4aded5f9e769b8e23ff69b47"
