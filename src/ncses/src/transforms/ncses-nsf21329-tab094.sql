-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State or location and agency - Alabama" AS state_or_location_and_agency_alabama,
    "Total - Alabama" AS total_alabama,
    "Intramurala - Alabama" AS intramurala_alabama,
    "Extramural - Industry - Alabama" AS extramural_industry_alabama,
    "Extramural - Industry-administered FFRDCs - Alabama" AS extramural_industry_administered_ffrdcs_alabama,
    "Extramural - Universities and colleges - Alabama" AS extramural_universities_and_colleges_alabama,
    "Extramural - University-administered FFRDCs - Alabama" AS extramural_university_administered_ffrdcs_alabama,
    "Extramural - Other nonprofits - Alabama" AS extramural_other_nonprofits_alabama,
    "Extramural - Nonprofit-administered FFRDCs - Alabama" AS extramural_nonprofit_administered_ffrdcs_alabama,
    "Extramural - State local governments - Alabama" AS extramural_state_local_governments_alabama
FROM "ncses-nsf21329-tab094"
