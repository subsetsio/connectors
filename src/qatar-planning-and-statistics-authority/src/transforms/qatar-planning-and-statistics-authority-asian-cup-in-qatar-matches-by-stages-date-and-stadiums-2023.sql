-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "stage",
    "date",
    "team_1",
    "team_2",
    "team_1_score",
    "team_2_score",
    "attendance",
    "stadium"
FROM "qatar-planning-and-statistics-authority-asian-cup-in-qatar-matches-by-stages-date-and-stadiums-2023"
