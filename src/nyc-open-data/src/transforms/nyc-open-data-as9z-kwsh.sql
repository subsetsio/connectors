-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "on_street",
    "from_st",
    "to_street",
    "completion_date",
    "type_of_change",
    "new_direction",
    "boro",
    "notes"
FROM "nyc-open-data-as9z-kwsh"
