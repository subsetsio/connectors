-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner" AS total_owner,
    "Total_Non_Owner" AS total_non_owner,
    "Single_Total" AS single_total,
    "Single_Owner" AS single_owner,
    "Single_Non_Owner" AS single_non_owner,
    "Married_Total" AS married_total,
    "Married_Owner" AS married_owner,
    "Married_Non_Owner" AS married_non_owner,
    "Widowed_Total" AS widowed_total,
    "Widowed_Owner" AS widowed_owner,
    "Widowed_Non_Owner" AS widowed_non_owner,
    "Divorced_Separated_Total" AS divorced_separated_total,
    "Divorced_Separated_Owner" AS divorced_separated_owner,
    "Divorced_Separated_Non_Owner" AS divorced_separated_non_owner
FROM "sg-data-d-5869964f85ada1f8f4c8ad33dbed4e21"
