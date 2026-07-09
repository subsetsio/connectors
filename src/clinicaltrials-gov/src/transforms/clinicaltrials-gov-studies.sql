-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per registered study; phase can contain multiple pipe-separated values for studies spanning phases.
SELECT
    "nct_id",
    "brief_title",
    "official_title",
    "overall_status",
    "why_stopped",
    "start_date",
    "primary_completion_date",
    "completion_date",
    "study_first_post_date",
    "last_update_post_date",
    "study_type",
    "phase",
    "enrollment_count",
    "enrollment_type",
    "allocation",
    "intervention_model",
    "primary_purpose",
    "masking",
    "sex",
    "minimum_age",
    "maximum_age",
    "healthy_volunteers",
    "lead_sponsor_name",
    "lead_sponsor_class",
    "responsible_party_type"
FROM "clinicaltrials-gov-studies"
