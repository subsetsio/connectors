-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Research and development - Any R and D - Number" AS research_and_development_any_r_and_d_number,
    "Research and development - Any R and D - SE" AS research_and_development_any_r_and_d_se,
    "Research and development - Basic research - Number" AS research_and_development_basic_research_number,
    "Research and development - Basic research - SE" AS research_and_development_basic_research_se,
    "Research and development - Applied research - Number" AS research_and_development_applied_research_number,
    "Research and development - Applied research - SE" AS research_and_development_applied_research_se,
    "Research and development - Experimental development - Number" AS research_and_development_experimental_development_number,
    "Research and development - Experimental development - SE" AS research_and_development_experimental_development_se,
    "Computer applications - Experimental development - Number" AS computer_applications_experimental_development_number,
    "Computer applications - Experimental development - SE" AS computer_applications_experimental_development_se,
    "Design - Experimental development - Number" AS design_experimental_development_number,
    "Design - Experimental development - SE" AS design_experimental_development_se,
    "Management sales or administrationa - Experimental development - Number" AS management_sales_or_administrationa_experimental_development_number,
    "Management sales or administrationa - Experimental development - SE" AS management_sales_or_administrationa_experimental_development_se,
    "Professional services - Experimental development - Number" AS professional_services_experimental_development_number,
    "Professional services - Experimental development - SE" AS professional_services_experimental_development_se,
    "Teaching - Experimental development - Number" AS teaching_experimental_development_number,
    "Teaching - Experimental development - SE" AS teaching_experimental_development_se,
    "Otherb - Experimental development - Number" AS otherb_experimental_development_number,
    "Otherb - Experimental development - SE" AS otherb_experimental_development_se
FROM "ncses-nsf25321-tab045-002"
