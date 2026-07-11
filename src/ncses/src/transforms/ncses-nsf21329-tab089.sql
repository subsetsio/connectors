-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State or location" AS state_or_location,
    "Total" AS total,
    "Intramurala" AS intramurala,
    "Extramural - Industry" AS extramural_industry,
    "Extramural - Industry-administered FFRDCs" AS extramural_industry_administered_ffrdcs,
    "Extramural - Universities and colleges" AS extramural_universities_and_colleges,
    "Extramural - University-administered FFRDCs" AS extramural_university_administered_ffrdcs,
    "Extramural - Other nonprofits" AS extramural_other_nonprofits,
    "Extramural - Nonprofit-administered FFRDCs" AS extramural_nonprofit_administered_ffrdcs,
    "Extramural - State local governments" AS extramural_state_local_governments
FROM "ncses-nsf21329-tab089"
