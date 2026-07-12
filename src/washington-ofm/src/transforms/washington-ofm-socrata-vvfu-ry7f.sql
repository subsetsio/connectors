-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Criminal justice records are published as source records without a verified natural key in this model; avoid treating row order as a stable identifier.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "county",
    CAST("indexyear" AS BIGINT) AS indexyear,
    "location",
    CAST("population" AS BIGINT) AS population,
    CAST("total" AS BIGINT) AS total,
    CAST("rate" AS DOUBLE) AS rate,
    CAST("prsntotal" AS BIGINT) AS prsntotal,
    CAST("prsnrate" AS DOUBLE) AS prsnrate,
    CAST("murder" AS BIGINT) AS murder,
    CAST("manslaughter" AS BIGINT) AS manslaughter,
    CAST("forcible_sex" AS BIGINT) AS forcible_sex,
    CAST("assault" AS BIGINT) AS assault,
    CAST("non_forcible_sex" AS BIGINT) AS non_forcible_sex,
    CAST("kidnapping_abduction" AS BIGINT) AS kidnapping_abduction,
    CAST("human_trafficking" AS BIGINT) AS human_trafficking,
    CAST("viol_of_no_contact" AS BIGINT) AS viol_of_no_contact,
    CAST("prprtytotal" AS BIGINT) AS prprtytotal,
    CAST("prprtyrate" AS DOUBLE) AS prprtyrate,
    CAST("arson" AS BIGINT) AS arson,
    CAST("bribery" AS BIGINT) AS bribery,
    CAST("burglary" AS BIGINT) AS burglary,
    CAST("counterfeiting_forgery" AS BIGINT) AS counterfeiting_forgery,
    CAST("destruction_of_property" AS BIGINT) AS destruction_of_property,
    CAST("extortion_blackmail" AS BIGINT) AS extortion_blackmail,
    CAST("robbery" AS BIGINT) AS robbery,
    CAST("theft" AS BIGINT) AS theft,
    CAST("sctytotal" AS BIGINT) AS sctytotal,
    CAST("sctyrate" AS DOUBLE) AS sctyrate,
    CAST("drug_violations" AS BIGINT) AS drug_violations,
    CAST("gambling_violations" AS BIGINT) AS gambling_violations,
    CAST("pornography" AS BIGINT) AS pornography,
    CAST("prostitution" AS BIGINT) AS prostitution,
    CAST("weapon_law_violation" AS BIGINT) AS weapon_law_violation,
    CAST("animal_cruelty" AS BIGINT) AS animal_cruelty
FROM "washington-ofm-socrata-vvfu-ry7f"
