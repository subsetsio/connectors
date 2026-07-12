-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "establishments_by_number_of_employees",
    "lmnshat_hsb_dd_lmshtglyn",
    "category",
    "lfy",
    "sub_category",
    "lfy_lfr_y",
    "total_000_q_r"
FROM "qatar-planning-and-statistics-authority-production-and-value-added-of-transportation-and-communication-activity-by-size-of-establishment"
