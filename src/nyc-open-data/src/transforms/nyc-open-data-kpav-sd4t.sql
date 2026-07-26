-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "job_id",
    "agency",
    "posting_type",
    "of_positions",
    "business_title",
    "civil_service_title",
    "title_classification",
    "title_code_no",
    "_level" AS level,
    "job_category",
    "fulltimeparttime_indicator",
    "career_level",
    "salary_range_from",
    "salary_range_to",
    "salary_frequency",
    "work_location",
    "divisionwork_unit",
    "job_description",
    "minimum_qual_requirements",
    "preferred_skills",
    "additional_information",
    "to_apply",
    "hoursshift",
    "work_location_1",
    "recruitment_contact",
    "residency_requirement",
    "posting_date",
    "post_until",
    "posting_updated",
    "process_date"
FROM "nyc-open-data-kpav-sd4t"
