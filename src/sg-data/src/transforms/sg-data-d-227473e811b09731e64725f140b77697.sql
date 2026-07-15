-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "licensee_name",
    "licence_number",
    "premises_address",
    "grade",
    "demerit_points",
    "suspension_start_date",
    "suspension_end_date"
FROM "sg-data-d-227473e811b09731e64725f140b77697"
