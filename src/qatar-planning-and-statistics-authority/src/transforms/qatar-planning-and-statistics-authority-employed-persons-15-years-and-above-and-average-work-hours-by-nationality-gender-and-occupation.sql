-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "occupation",
    "lmhn",
    "employed_persons",
    "average_work_hours"
FROM "qatar-planning-and-statistics-authority-employed-persons-15-years-and-above-and-average-work-hours-by-nationality-gender-and-occupation"
