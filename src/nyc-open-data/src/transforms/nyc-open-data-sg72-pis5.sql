-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "initiative_category",
    "initiative_detailed",
    "budget_2021",
    "spent_2021",
    "budget_2022",
    "spent_2022",
    "budget_2023",
    "spent_2023",
    "budget_2024",
    "spent_2024",
    "budget_2025"
FROM "nyc-open-data-sg72-pis5"
