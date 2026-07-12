-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "fy_t_l_mr_blsnwt",
    "age_groups_in_years",
    "ljnsy",
    "nationality",
    "lhl_lt_lymy",
    "educational_status",
    "ljns",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-employee-trainees-who-received-training-at-private-training-centers-by-educational-status-gender"
