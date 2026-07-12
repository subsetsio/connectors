-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "craft_workers",
    "elementary_occupations",
    "plant_and_machine_operators",
    "professionals",
    "clerks"
FROM "qatar-planning-and-statistics-authority-number-of-labor-force-15-years-by-occupation-thousand"
