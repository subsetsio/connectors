-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "service_provider_english",
    "service_provider_arabic",
    "title_english",
    "title_arabic",
    "users_by_year",
    "page_views",
    "created_date",
    "recent_updation_date",
    "service_mode",
    "page_url_arabic",
    "page_url_english",
    "external_url_arabic",
    "external_url_english"
FROM "qatar-planning-and-statistics-authority-government-e-services-directory-with-usage-statistics"
