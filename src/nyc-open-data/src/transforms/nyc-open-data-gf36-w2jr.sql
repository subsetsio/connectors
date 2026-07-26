-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "category",
    "average_pe_class_size",
    "average_of_days_per_week",
    "average_of_minutes_per_week",
    "total_of_students",
    "total_of_students_who_received_or_were_scheduled_to_receive_the_required_amount_of_pe_instruction_as_of_february_26_2020",
    "of_students_who_received_or_were_scheduled_to_receive_the_required_amount_of_pe_instruction_as_of_february_26_2020"
FROM "nyc-open-data-gf36-w2jr"
