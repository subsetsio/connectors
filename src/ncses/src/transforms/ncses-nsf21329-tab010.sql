-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Agency - Department of Defense" AS agency_department_of_defense,
    "Total - Department of Defense" AS total_department_of_defense,
    "Intramurala - Department of Defense" AS intramurala_department_of_defense,
    "Extramural - United States and U.S. territories - Industry - Department of Defense" AS extramural_united_states_and_u_s_territories_industry_department_of_defense,
    "Extramural - United States and U.S. territories - Industry-administered FFRDCs - Department of Defense" AS extramural_united_states_and_u_s_territories_industry_administered_ffrdcs_department_of_defense,
    "Extramural - United States and U.S. territories - Universities and colleges - Department of Defense" AS extramural_united_states_and_u_s_territories_universities_and_colleges_department_of_defense,
    "Extramural - United States and U.S. territories - University-administered FFRDCs - Department of Defense" AS extramural_united_states_and_u_s_territories_university_administered_ffrdcs_department_of_defense,
    "Extramural - United States and U.S. territories - Other nonprofits - Department of Defense" AS extramural_united_states_and_u_s_territories_other_nonprofits_department_of_defense,
    "Extramural - United States and U.S. territories - Nonprofit-administered FFRDCs - Department of Defense" AS extramural_united_states_and_u_s_territories_nonprofit_administered_ffrdcs_department_of_defense,
    "Extramural - United States and U.S. territories - State local governments - Department of Defense" AS extramural_united_states_and_u_s_territories_state_local_governments_department_of_defense,
    "Extramural - Foreign - State local governments - Department of Defense" AS extramural_foreign_state_local_governments_department_of_defense
FROM "ncses-nsf21329-tab010"
