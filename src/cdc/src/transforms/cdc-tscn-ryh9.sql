-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geographic aggregation" AS geographic_aggregation,
    "Week Ending Date" AS week_ending_date,
    CAST("Number of Residents Up To Date with COVID-19 Vaccines" AS BIGINT) AS number_of_residents_up_to_date_with_covid_19_vaccines,
    CAST("Total Number of Residents" AS BIGINT) AS total_number_of_residents,
    CAST("Number of COVID-19 Positive Residents" AS BIGINT) AS number_of_covid_19_positive_residents,
    CAST("Number of COVID-19 Positive Residents Up To Date with COVID-19 Vaccines" AS BIGINT) AS number_of_covid_19_positive_residents_up_to_date_with_covid_19_vaccines,
    CAST("Number of Hospitalized COVID-19 Positive Residents" AS BIGINT) AS number_of_hospitalized_covid_19_positive_residents,
    CAST("Number of Hospitalized COVID-19 Positive Residents Up To Date with COVID-19 Vaccines" AS BIGINT) AS number_of_hospitalized_covid_19_positive_residents_up_to_date_with_covid_19_vaccines,
    CAST("Percent of Residents Up To Date with COVID-19 Vaccines" AS DOUBLE) AS percent_of_residents_up_to_date_with_covid_19_vaccines,
    CAST("Number of Facilities Reporting" AS BIGINT) AS number_of_facilities_reporting,
    CAST("Number of Residents who have received Influenza Vaccine" AS BIGINT) AS number_of_residents_who_have_received_influenza_vaccine,
    CAST("Number of Influenza Positive Residents" AS BIGINT) AS number_of_influenza_positive_residents,
    CAST("Number of Influenza Positive Residents who have received Influenza Vaccine" AS BIGINT) AS number_of_influenza_positive_residents_who_have_received_influenza_vaccine,
    CAST("Number of Hospitalized Influenza Positive Residents" AS BIGINT) AS number_of_hospitalized_influenza_positive_residents,
    CAST("Number of Hospitalized Influenza Positive Residents who have received Influenza Vaccine" AS BIGINT) AS number_of_hospitalized_influenza_positive_residents_who_have_received_influenza_vaccine,
    CAST("Percent of Residents who have received Influenza Vaccine" AS DOUBLE) AS percent_of_residents_who_have_received_influenza_vaccine,
    CAST("Number of Residents who have received RSV Vaccine" AS BIGINT) AS number_of_residents_who_have_received_rsv_vaccine,
    CAST("Number of RSV Positive Residents" AS BIGINT) AS number_of_rsv_positive_residents,
    CAST("Number of RSV Positive Residents who have received RSV Vaccine" AS BIGINT) AS number_of_rsv_positive_residents_who_have_received_rsv_vaccine,
    CAST("Number of Hospitalized RSV Positive Residents" AS BIGINT) AS number_of_hospitalized_rsv_positive_residents,
    CAST("Number of Hospitalized RSV Positive Residents who have received RSV Vaccine" AS BIGINT) AS number_of_hospitalized_rsv_positive_residents_who_have_received_rsv_vaccine,
    CAST("Percent of Residents who have received RSV Vaccine" AS DOUBLE) AS percent_of_residents_who_have_received_rsv_vaccine
FROM "cdc-tscn-ryh9"
