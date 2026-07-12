-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "occupation",
    "lmhn",
    "15_19",
    "20_24",
    "25_29",
    "30_34",
    "35_39",
    "40_44",
    "50_54",
    "45_49",
    "60_65",
    "55_59",
    "65",
    "total",
    "total_in_percent",
    "skill_level",
    "skill_level_ar"
FROM "qatar-planning-and-statistics-authority-economically-active-qatari-population-15-years-and-above-by-status-in-employment-and-occupation"
