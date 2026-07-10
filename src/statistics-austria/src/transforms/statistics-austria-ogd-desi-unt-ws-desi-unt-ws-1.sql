-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "federal_states",
    "economy_sector",
    "enterprises_providing_ict_related_training_to_their_employees",
    "sme_with_at_least_basic_level_of_digital_intensity",
    "enterprises_sharing_information_electronically",
    "enterprises_using_at_least_two_social_media_channels",
    "enterprises_performing_data_analytics",
    "enterprises_using_cloud_services",
    "enterprises_using_technologies_based_on_artificial_intelligence",
    "enterprises_using_cloud_services_or_technologies_based_on_artificial_intelligence_or_performing_data_analytics",
    "enterprises_sending_e_invoices_suitable_for_automated_processing",
    "sme_selling_via_websites_apps_or_online_marketplaces",
    "sales_via_e_commerce_by_smes",
    "sme_selling_via_websites_apps_or_online_marketplaces_to_other_eu_countries"
FROM "statistics-austria-ogd-desi-unt-ws-desi-unt-ws-1"
