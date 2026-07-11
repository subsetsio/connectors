-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristics" AS characteristics,
    "Total" AS total,
    "STEM occupation - S and E" AS stem_occupation_s_and_e,
    "STEM occupation - S and E related" AS stem_occupation_s_and_e_related,
    "STEM occupation - STEM middle skill" AS stem_occupation_stem_middle_skill,
    "Non-STEM occupation - STEM middle skill" AS non_stem_occupation_stem_middle_skill
FROM "ncses-nsf25323-tab005"
