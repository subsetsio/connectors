-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Title" AS title,
    "Associated PRC" AS associated_prc,
    CAST("Resource Publication Year" AS BIGINT) AS resource_publication_year,
    "Project Year Range" AS project_year_range,
    "Type of Resource" AS type_of_resource,
    "Description" AS description,
    "File Type" AS file_type,
    "Audience For Resource" AS audience_for_resource,
    "Health Topics" AS health_topics,
    "Population Characteristics" AS population_characteristics,
    "Social Determinants of Health" AS social_determinants_of_health,
    "Applied Settings" AS applied_settings,
    "Geographic Identifier" AS geographic_identifier,
    "Primary Goal of Resource" AS primary_goal_of_resource,
    "Contact/Email" AS contact_email,
    "Link To Resource" AS link_to_resource
FROM "cdc-2m7c-st88"
