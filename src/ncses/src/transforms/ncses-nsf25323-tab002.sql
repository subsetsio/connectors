-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Demographic characteristics" AS demographic_characteristics,
    "Total" AS total,
    "U.S. Labor force - Employed - STEM occupation - S and E" AS u_s_labor_force_employed_stem_occupation_s_and_e,
    "U.S. Labor force - Employed - STEM occupation - S and E related" AS u_s_labor_force_employed_stem_occupation_s_and_e_related,
    "U.S. Labor force - Employed - STEM occupation - STEM middle skill" AS u_s_labor_force_employed_stem_occupation_stem_middle_skill,
    "U.S. Labor force - Employed - Non-STEM occupation - STEM middle skill" AS u_s_labor_force_employed_non_stem_occupation_stem_middle_skill,
    "U.S. Labor force - Unemployed - Non-STEM occupation - STEM middle skill" AS u_s_labor_force_unemployed_non_stem_occupation_stem_middle_skill,
    "Not in the U.S. labor force - Unemployed - Non-STEM occupation - STEM middle skill" AS not_in_the_u_s_labor_force_unemployed_non_stem_occupation_stem_middle_skill
FROM "ncses-nsf25323-tab002"
