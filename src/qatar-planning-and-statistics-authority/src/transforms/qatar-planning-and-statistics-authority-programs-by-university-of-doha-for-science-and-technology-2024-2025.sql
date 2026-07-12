-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "college",
    "credential",
    "degree_abbv",
    "program_name_english",
    "program_name_arabic",
    "duration_years",
    "website_link",
    "subject_covered"
FROM "qatar-planning-and-statistics-authority-programs-by-university-of-doha-for-science-and-technology-2024-2025"
