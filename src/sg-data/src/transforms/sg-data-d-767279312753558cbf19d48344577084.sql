-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "licence_no",
    "product_name",
    "license_holder",
    "approval_d",
    "forensic_classification",
    "atc_code",
    "dosage_form",
    "route_of_administration",
    "manufacturer",
    "country_of_manufacturer",
    "active_ingredients",
    "strength"
FROM "sg-data-d-767279312753558cbf19d48344577084"
