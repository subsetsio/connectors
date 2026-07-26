-- Accepted GENESIS table currently returns an FFCSV header with no data rows.
-- Keep a structural transform so the download/transform graph stays complete;
-- the active spec waiver excuses this table until upstream restores rows.
SELECT
    CAST("statistics_code" AS BIGINT) AS statistics_code,
    "statistics_label",
    "time_code",
    "time_label",
    CAST("time" AS BIGINT) AS time,
    "1_variable_code",
    "1_variable_label",
    CAST("1_variable_attribute_code" AS BIGINT) AS "1_variable_attribute_code",
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
FROM "statistisches-landesamt-sachsen-anhalt-52111-0002"
