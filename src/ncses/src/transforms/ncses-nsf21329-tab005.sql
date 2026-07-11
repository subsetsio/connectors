-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total R and D" AS total_r_and_d,
    "Basic research" AS basic_research,
    "Applied research" AS applied_research,
    "Experimental development - Total" AS experimental_development_total,
    "Experimental development - Advanced technology" AS experimental_development_advanced_technology,
    "Experimental development - Major systems" AS experimental_development_major_systems
FROM "ncses-nsf21329-tab005"
