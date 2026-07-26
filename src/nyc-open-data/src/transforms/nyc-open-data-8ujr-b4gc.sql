-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "borough",
    "applications_for_general_vending_licenses_from_veterans_received_dcwp",
    "applications_for_general_vending_licenses_from_veterans_approved_dcwp",
    "applications_for_general_vending_licenses_from_veterans_rejected_dcwp",
    "civil_service_exam_applicants_claiming_veterans_credit_dcas",
    "licenses_and_permits_issued_to_veterans_feeexempt_mobile_food_vending_licenses_dohmh",
    "licenses_and_permits_issued_to_veterans_food_vending_permits_dohmh",
    "mitchelllama_applications_from_veteranssurviving_spouses_heads_of_household_received_hpd",
    "mitchelllama_applications_from_veteranssurviving_spouses_heads_of_household_approved_hpd",
    "mitchelllama_applications_from_veteranssurviving_spouses_heads_of_household_rejected_hpd",
    "use_of_hudvash_vouchers_in_rental_housing_administered_by_hpd_hpd",
    "use_of_hudvash_vouchers_in_nycha_housing_administered_by_nycha_nycha",
    "use_of_hudvash_vouchers_in_rental_units_administered_by_nycha_nycha"
FROM "nyc-open-data-8ujr-b4gc"
