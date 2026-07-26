-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "category",
    "average_of_students_per_pe_class",
    "total_of_students",
    "total_of_students_who_received_pe_instruction_in_all_terms",
    "of_students_who_received_pe_instruction_in_all_terms"
FROM "nyc-open-data-s47t-kwt5"
