-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "type_of_phone_call_into_borough_hall",
    "number_of_calls",
    "additional_notes_where_applicable_include_the_range_of_possible_values_units_of_measure_how_to_interpret_nullzero_values_whether_there_are_specific_relationships_between_columns_and_information_on_column_source"
FROM "nyc-open-data-y6ds-67d5"
