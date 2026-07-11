-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All social sciences fields" AS all_social_sciences_fields,
    "Anthropology" AS anthropology,
    "Area ethnic cultural gender and group studies" AS area_ethnic_cultural_gender_and_group_studies,
    "Economics" AS economics,
    "Political science and government" AS political_science_and_government,
    "Public policy analysis" AS public_policy_analysis,
    "Sociology demography and population studies" AS sociology_demography_and_population_studies,
    "Social sciences other" AS social_sciences_other
FROM "ncses-nsf25349-tab008-013"
