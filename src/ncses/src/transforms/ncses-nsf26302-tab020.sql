-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State and department or agency" AS state_and_department_or_agency,
    "All R and D expenditures" AS all_r_and_d_expenditures,
    "Intramural performersa" AS intramural_performersa,
    "Extramural performersb - Total" AS extramural_performersb_total,
    "Extramural performersb - Higher education institutions" AS extramural_performersb_higher_education_institutions,
    "Extramural performersb - Companies and individualsc" AS extramural_performersb_companies_and_individualsc,
    "Extramural performersb - Nonprofit organizationsd" AS extramural_performersb_nonprofit_organizationsd,
    "Extramural performersb - Other governmentse" AS extramural_performersb_other_governmentse,
    "Extramural performersb - All otherf" AS extramural_performersb_all_otherf
FROM "ncses-nsf26302-tab020"
