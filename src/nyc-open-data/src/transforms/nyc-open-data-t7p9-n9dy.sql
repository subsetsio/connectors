-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "week_start_date",
    "agency",
    "final_incident_type",
    "of_incidents_calculated",
    "call_to_first_pickup",
    "call_to_pd_calltaker_handoff",
    "call_to_fdny_pickup",
    "call_to_fdny_job_creation",
    "call_to_ems_pickup",
    "call_to_agency_job_creation",
    "call_to_agency_dispatch",
    "call_to_agency_arrival",
    "call_to_first_arrival_multiagency_incidents",
    "median_pickup",
    "median_calltaker_handoff",
    "median_fdny_pickup",
    "median_fdny_job_creation",
    "median_ems_pickup",
    "median_ems_job_creation",
    "median_dispatch",
    "median_travel",
    "median_cumulative_first_arrival_multiagency_incidents",
    "average_travel",
    "average_dispatch",
    "average_ems_processing",
    "average_ems_pickup",
    "average_calltaker_processing",
    "average_pickup",
    "average_fd_pickup",
    "average_fd_processing"
FROM "nyc-open-data-t7p9-n9dy"
