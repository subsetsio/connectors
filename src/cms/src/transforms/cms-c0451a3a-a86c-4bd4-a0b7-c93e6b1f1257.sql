-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Title" AS title,
    "Author" AS author,
    "URL" AS url,
    "Month of Publication" AS month_of_publication,
    CAST("Year of publication" AS BIGINT) AS year_of_publication,
    "Abstract" AS abstract,
    "Keywords" AS keywords,
    "Type" AS type,
    "Related Content" AS related_content,
    "Related Content 2" AS related_content_2,
    "Related Content 3" AS related_content_3,
    "Related Content 4" AS related_content_4,
    "Related Content 5" AS related_content_5,
    "At-A-Glance Reports URL" AS at_a_glance_reports_url,
    "At-A-Glance Reports" AS at_a_glance_reports,
    "Perspective Report URL" AS perspective_report_url,
    "Perspective Report" AS perspective_report,
    CAST("ID" AS BIGINT) AS id
FROM "cms-c0451a3a-a86c-4bd4-a0b7-c93e6b1f1257"
