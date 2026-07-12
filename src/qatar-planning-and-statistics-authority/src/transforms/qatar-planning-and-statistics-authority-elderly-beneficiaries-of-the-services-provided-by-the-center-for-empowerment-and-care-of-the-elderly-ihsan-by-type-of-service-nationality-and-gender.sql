-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_services_ar",
    "qataris_males_2019",
    "qataris_females_2019",
    "non_qataris_males_2019",
    "non_qataris_females_2019",
    "qataris_males_2020",
    "qataris_females_2020",
    "non_qataris_males_2020",
    "non_qataris_females_2020",
    "qataris_males_2021",
    "qataris_females_2021",
    "non_qataris_males_2021",
    "non_qataris_females_2021",
    "qataris_males_2022",
    "qataris_females_2022",
    "non_qataris_males_2022",
    "non_qataris_females_2022",
    "qataris_males_2023",
    "qataris_females_2023",
    "non_qataris_males_2023",
    "non_qataris_females_2023",
    "type_of_service"
FROM "qatar-planning-and-statistics-authority-elderly-beneficiaries-of-the-services-provided-by-the-center-for-empowerment-and-care-of-the-elderly-ihsan-by-type-of-service-nationality-and-gender"
