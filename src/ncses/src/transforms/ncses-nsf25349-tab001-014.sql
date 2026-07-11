-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "High school or less" AS high_school_or_less,
    "Some collegea" AS some_collegea,
    "Bachelor's degree" AS bachelor_s_degree,
    "Master's degree" AS master_s_degree,
    "Professional doctorateb" AS professional_doctorateb,
    "Research doctorate" AS research_doctorate
FROM "ncses-nsf25349-tab001-014"
