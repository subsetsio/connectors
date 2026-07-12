-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table is wide by offence type; sum only comparable offence columns and avoid adding derived totals to their components.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Crimes_Excluding_Drug_Offenses" AS BIGINT) AS crimes_excluding_drug_offenses,
    CAST("Drug_Offences_Classified_Under_Crimes" AS BIGINT) AS drug_offences_classified_under_crimes,
    CAST("Misdemeanours_Excluding_Drug_Offences" AS BIGINT) AS misdemeanours_excluding_drug_offences,
    CAST("Drug_Offences_Classified_Under_Misdemeanours" AS BIGINT) AS drug_offences_classified_under_misdemeanours,
    CAST("Contraventions_Excluding_Road_Traffic" AS BIGINT) AS contraventions_excluding_road_traffic,
    CAST("Road_Traffic_Contraventions" AS BIGINT) AS road_traffic_contraventions,
    CAST("Other_Occurrences" AS BIGINT) AS other_occurrences,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-cases-reported-offences-type-republic-mauritius-2007-2017"
