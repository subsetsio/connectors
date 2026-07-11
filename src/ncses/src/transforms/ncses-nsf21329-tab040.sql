-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Intramurala" AS intramurala,
    "Extramural - United States and U.S. territories - Industry" AS extramural_united_states_and_u_s_territories_industry,
    "Extramural - United States and U.S. territories - Industry-administered FFRDCs" AS extramural_united_states_and_u_s_territories_industry_administered_ffrdcs,
    "Extramural - United States and U.S. territories - Universities and colleges" AS extramural_united_states_and_u_s_territories_universities_and_colleges,
    "Extramural - United States and U.S. territories - University-administered FFRDCs" AS extramural_united_states_and_u_s_territories_university_administered_ffrdcs,
    "Extramural - United States and U.S. territories - Other nonprofits" AS extramural_united_states_and_u_s_territories_other_nonprofits,
    "Extramural - United States and U.S. territories - Nonprofit-administered FFRDCs" AS extramural_united_states_and_u_s_territories_nonprofit_administered_ffrdcs,
    "Extramural - United States and U.S. territories - State local governments" AS extramural_united_states_and_u_s_territories_state_local_governments,
    "Extramural - Foreign - State local governments" AS extramural_foreign_state_local_governments
FROM "ncses-nsf21329-tab040"
