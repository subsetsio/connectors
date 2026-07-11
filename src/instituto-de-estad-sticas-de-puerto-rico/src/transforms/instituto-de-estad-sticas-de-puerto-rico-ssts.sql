-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "ESTABLISHMENT NUMBER" AS establishment_number,
    "ESTABLISHMENT NAME" AS establishment_name,
    "ESTABLISHMENT SITE ADDRESS LINE 1" AS establishment_site_address_line_1,
    "EST. SITE ADDRESS LINE 2" AS est_site_address_line_2,
    "EST. SITE CITY" AS est_site_city,
    "EST. SITE STATE" AS est_site_state,
    "EST. SITE ZIP" AS est_site_zip,
    "EST. SITE COUNTY" AS est_site_county,
    "EST. SITE COUNTRY" AS est_site_country,
    CAST("EPA REGION" AS BIGINT) AS epa_region,
    "ESTABLISHMENT MAILING ADDRESS LINE 1" AS establishment_mailing_address_line_1,
    "EST. MAILING ADDRESS LINE 2" AS est_mailing_address_line_2,
    "EST. MAIL CITY" AS est_mail_city,
    "EST. MAIL STATE" AS est_mail_state,
    "EST. MAIL ZIP" AS est_mail_zip,
    "EST. MAIL COUNTRY" AS est_mail_country,
    "COMPANY NAME" AS company_name,
    "COMPANY SITE ADDRESS LINE 1" AS company_site_address_line_1,
    "CO. SITE ADDRESS LINE 2" AS co_site_address_line_2,
    "CO. SITE CITY" AS co_site_city,
    "CO. SITE STATE" AS co_site_state,
    "CO. SITE ZIP" AS co_site_zip,
    "CO. SITE COUNTRY" AS co_site_country,
    "COMPANY MAILING ADDRESS LINE 1" AS company_mailing_address_line_1,
    "CO. MAIL ADDRESS LINE 2" AS co_mail_address_line_2,
    "CO. MAIL CITY" AS co_mail_city,
    "CO. MAIL STATE" AS co_mail_state,
    "CO. MAIL ZIP" AS co_mail_zip,
    "CO. MAIL COUNTRY" AS co_mail_country
FROM "instituto-de-estad-sticas-de-puerto-rico-ssts"
