-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include multiple institution aggregation levels, including statewide and local entities; filter entity scope before aggregating enrollment.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "pk",
    "pkhalf",
    "pkfull",
    "khalf",
    "kfull",
    "n_1",
    "n_2",
    "n_3",
    "n_4",
    "n_5",
    "n_6",
    "n_7",
    "n_8",
    "n_9",
    "n_10",
    "n_11",
    "n_12",
    "uge",
    "ugs",
    "k12"
FROM "new-york-state-education-department-enrollment-beds-day"
