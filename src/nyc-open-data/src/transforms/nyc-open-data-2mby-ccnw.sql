-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "as_of_date",
    "complaint_id",
    "incident_date",
    "incident_hour",
    "ccrb_received_date",
    "close_date",
    "borough_of_incident_occurrence",
    "precinct_of_incident_occurrence",
    "location_type_of_incident",
    "reason_for_police_contact",
    "outcome_of_police_encounter",
    "ccrb_complaint_disposition",
    "bwc_evidence",
    "video_evidence"
FROM "nyc-open-data-2mby-ccnw"
