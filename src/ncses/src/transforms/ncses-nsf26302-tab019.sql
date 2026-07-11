-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State and department or agency" AS state_and_department_or_agency,
    "R and D expenditures for intramural performers" AS r_and_d_expenditures_for_intramural_performers,
    "Source of funds - Federal government" AS source_of_funds_federal_government,
    "Source of funds - Own state government" AS source_of_funds_own_state_government,
    "Source of funds - Other nonfederal governments" AS source_of_funds_other_nonfederal_governments,
    "Source of funds - Nonprofit organizations" AS source_of_funds_nonprofit_organizations,
    "Source of funds - Businesses and individuals" AS source_of_funds_businesses_and_individuals,
    "Source of funds - Higher education institutions" AS source_of_funds_higher_education_institutions
FROM "ncses-nsf26302-tab019"
