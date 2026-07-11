-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "R and D expendituresa - All R and D expenditures" AS r_and_d_expendituresa_all_r_and_d_expenditures,
    "R and D expendituresa - Intramural performersb" AS r_and_d_expendituresa_intramural_performersb,
    "R and D expendituresa - Extramural performersc - Total" AS r_and_d_expendituresa_extramural_performersc_total,
    "R and D expendituresa - Extramural performersc - Higher education institutions" AS r_and_d_expendituresa_extramural_performersc_higher_education_institutions,
    "R and D expendituresa - Extramural performersc - Companies and individualsd" AS r_and_d_expendituresa_extramural_performersc_companies_and_individualsd,
    "R and D expendituresa - Extramural performersc - Nonprofit organizationse" AS r_and_d_expendituresa_extramural_performersc_nonprofit_organizationse,
    "R and D expendituresa - Extramural performersc - Other governmentsf" AS r_and_d_expendituresa_extramural_performersc_other_governmentsf,
    "R and D expendituresa - Extramural performersc - All otherg" AS r_and_d_expendituresa_extramural_performersc_all_otherg,
    "R and D plant expendituresh - Extramural performersc - All R and D plant expenditures" AS r_and_d_plant_expendituresh_extramural_performersc_all_r_and_d_plant_expenditures,
    "R and D plant expendituresh - Extramural performersc - Intramural" AS r_and_d_plant_expendituresh_extramural_performersc_intramural,
    "R and D plant expendituresh - Extramural performersc - Extramural" AS r_and_d_plant_expendituresh_extramural_performersc_extramural
FROM "ncses-nsf26302-tab002"
