-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pub_date",
    "boro",
    "managing_agcy_cd",
    "managing_agcy",
    "project_id",
    "project_descr",
    "seq_number",
    "task_description",
    "orig_start_date",
    "orig_end_date",
    "task_start_date",
    "task_end_date"
FROM "nyc-open-data-s7yh-frbm"
