-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "borough",
    "geographic_subset",
    "geographic_identifier",
    "client_died",
    "does_not_reside_in_nyc",
    "no_risk",
    "referred_person_has_sufficient_mental_and_physical_capacity",
    "referred_person_retains_decisionmaking_capacity_and_is_refusing_all_offers_of_assistance",
    "someone_else_willing_and_able_responsibly",
    "unable_to_locate",
    "under_18",
    "total_ineligible_by_geographic_subset",
    "client_died_by_geographic_subset",
    "does_not_reside_in_nyc_by_geographic_subset",
    "no_risk_by_geographic_subset",
    "referred_person_has_sufficient_mental_and_physical_capacity_by_geographic_subset",
    "referred_person_retains_decisionmaking_capacity_and_is_refusing_all_offers_of_assistance_by_geographic_subset",
    "someone_else_willing_and_able_responsibly_by_geographic_subset",
    "unable_to_locate_by_geographic_subset",
    "under_18_by_geographic_subset",
    "total_ineligible_referrals_by_geographic_subset",
    "client_died_citywide",
    "does_not_reside_in_nyc_citywide",
    "no_risk_citywide",
    "referred_person_has_sufficient_mental_and_physical_capacity_citywide",
    "referred_person_retains_decisionmaking_capacity_and_is_refusing_all_offers_of_assistance_citywide",
    "someone_else_willing_and_able_responsibly_citywide",
    "unable_to_locate_citywide",
    "under_18_citywide",
    "total_ineligible_referrals_citywide"
FROM "nyc-open-data-vibf-3qrq"
