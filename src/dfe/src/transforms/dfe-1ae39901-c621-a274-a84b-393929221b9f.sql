-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "old_la_code",
    "new_la_code",
    "la_name",
    "version",
    CAST("education_investment_area_flag" AS BIGINT) AS education_investment_area_flag,
    CAST("priority_area_flag" AS BIGINT) AS priority_area_flag,
    "establishment_type_group",
    "breakdown_topic",
    "sex",
    "qualification_type",
    "subject",
    "grade",
    "number_achieving",
    "percentage_achieving"
FROM "dfe-1ae39901-c621-a274-a84b-393929221b9f"
