-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hmp_index",
    "title",
    "description_of_action",
    "description_of_problem",
    "managing_agency",
    "supporting_agencies",
    "action_category",
    "action_status",
    "action_status_date",
    "hazards_addressed",
    "estimated_start",
    "estimated_finish",
    "estimated_cost",
    "federal_funding_source",
    "state_funding_source",
    "city_funding_source",
    "private_funding_source",
    "other_funding_source",
    "description_of_social_vulnerability_addressed",
    "description_of_critical_facility",
    "planning_regulation_capability",
    "administrative_technical_capability",
    "financial_capability",
    "education_outreach_capability",
    "contact_name",
    "contact_email",
    "web_link",
    "notes"
FROM "nyc-open-data-veqt-eu3t"
