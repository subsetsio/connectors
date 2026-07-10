SELECT
    CAST("competent_authority_organization_name" AS VARCHAR) AS "competent_authority_organization_name",
    CAST("competent_authority_website" AS VARCHAR) AS "competent_authority_website",
    CAST("designation_type_category" AS VARCHAR) AS "designation_type_category",
    CAST("designation_type_code" AS VARCHAR) AS "designation_type_code",
    CAST("designation_type_name" AS VARCHAR) AS "designation_type_name",
    CAST("designation_type_name_english" AS VARCHAR) AS "designation_type_name_english",
    CAST("legal_reference_level" AS VARCHAR) AS "legal_reference_level",
    CAST("legal_reference_link" AS VARCHAR) AS "legal_reference_link",
    CAST("legal_reference_name" AS VARCHAR) AS "legal_reference_name",
    CAST("legal_reference_official_journal_identification" AS VARCHAR) AS "legal_reference_official_journal_identification",
    CAST("legal_reference_publication_date" AS VARCHAR) AS "legal_reference_publication_date",
    CAST("national_designation_description" AS VARCHAR) AS "national_designation_description",
    CAST("remark" AS VARCHAR) AS "remark",
    CAST("remark_source" AS VARCHAR) AS "remark_source"
FROM "european-environment-agency-eunis.natda-designation-type"
