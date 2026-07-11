-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total intramural R and D 2019" AS total_intramural_r_and_d_2019,
    "Personnel costs 2019 - Amount" AS personnel_costs_2019_amount,
    "Personnel costs 2019 - % of total" AS personnel_costs_2019_of_total,
    "Total intramural R and D 2020 - % of total" AS total_intramural_r_and_d_2020_of_total,
    "Personnel costs 2020 - Amount" AS personnel_costs_2020_amount,
    "Personnel costs 2020 - % of total" AS personnel_costs_2020_of_total
FROM "ncses-nsf21329-tab095"
