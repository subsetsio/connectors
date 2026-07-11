-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Fiscal year" AS fiscal_year,
    "Total - All R and D expenditures" AS total_all_r_and_d_expenditures,
    "Total - Basic research" AS total_basic_research,
    "Total - Applied research" AS total_applied_research,
    "Total - Experimental development" AS total_experimental_development,
    "Federal - All R and D expenditures" AS federal_all_r_and_d_expenditures,
    "Federal - Basic research" AS federal_basic_research,
    "Federal - Applied research" AS federal_applied_research,
    "Federal - Experimental development" AS federal_experimental_development,
    "Nonfederal - All R and D expenditures" AS nonfederal_all_r_and_d_expenditures,
    "Nonfederal - Basic research" AS nonfederal_basic_research,
    "Nonfederal - Applied research" AS nonfederal_applied_research,
    "Nonfederal - Experimental development" AS nonfederal_experimental_development
FROM "ncses-nsf26304-tab008"
