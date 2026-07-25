-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_element_name",
    "preferred_physical_name",
    "subject_category_code",
    "description_text",
    "data_type_code",
    CAST("maximum_length" AS BIGINT) AS maximum_length,
    CAST("precision_number" AS BIGINT) AS precision_number,
    "pattern_text",
    "unit_of_measure",
    "value_domain",
    "business_owner_name",
    "data_asset_abbreviation",
    "data_asset_name",
    "system_number"
FROM "u-s-department-of-transportation-nhvr-exvq"
