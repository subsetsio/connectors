-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GENESIS dimension labels and codes are denormalized in the fact table; filter the relevant attribute columns before aggregating.
SELECT
    CAST("statistics_code" AS BIGINT) AS statistics_code,
    "statistics_label",
    "time_code",
    "time_label",
    CAST("time" AS BIGINT) AS time,
    "1_variable_code",
    "1_variable_label",
    CAST("1_variable_attribute_code" AS BIGINT) AS 1_variable_attribute_code,
    "1_variable_attribute_label",
    "2_variable_code",
    "2_variable_label",
    "2_variable_attribute_code",
    "2_variable_attribute_label",
    CAST("value" AS BIGINT) AS value,
    "value_unit",
    "value_variable_code",
    "value_variable_label",
    "source_table_code",
    "source_row_number"
FROM "statistisches-landesamt-sachsen-anhalt-12411-0001"
