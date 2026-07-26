-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_name",
    "address1",
    "city",
    "state",
    "zip_code",
    "borough",
    "neighborhood",
    "phone1",
    "fax",
    "website",
    "job_placement_services",
    "financial_aid_services",
    "contact_firstname",
    "contact_lastname",
    "course_name",
    "coursedescription",
    "keywords",
    "cost_total",
    "cost_includes",
    "cost_does_not_include",
    "duration",
    "duration_unit",
    "numhours",
    "prerequisites",
    "max_class_size",
    "years_course_offered",
    "instructor_credentials",
    "delivery_method",
    "schedule",
    "is_hra",
    "is_sbs"
FROM "nyc-open-data-fgq8-am2v"
