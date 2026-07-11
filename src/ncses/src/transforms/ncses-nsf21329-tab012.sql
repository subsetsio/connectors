-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "R and D - Total" AS r_and_d_total,
    "R and D - Industry-administered FFRDCs" AS r_and_d_industry_administered_ffrdcs,
    "R and D - University-administered FFRDCs" AS r_and_d_university_administered_ffrdcs,
    "R and D - Nonprofit-administered FFRDCs" AS r_and_d_nonprofit_administered_ffrdcs,
    "R and D plant - Total" AS r_and_d_plant_total,
    "R and D plant - Industry-administered FFRDCs" AS r_and_d_plant_industry_administered_ffrdcs,
    "R and D plant - University-administered FFRDCs" AS r_and_d_plant_university_administered_ffrdcs,
    "R and D plant - Nonprofit-administered FFRDCs" AS r_and_d_plant_nonprofit_administered_ffrdcs
FROM "ncses-nsf21329-tab012"
