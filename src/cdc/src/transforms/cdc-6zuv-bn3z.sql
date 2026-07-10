-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UniqueID" AS BIGINT) AS uniqueid,
    "Agency_Type" AS agency_type,
    CAST("Population_Served" AS BIGINT) AS population_served,
    CAST("No_Food_Estab" AS BIGINT) AS no_food_estab,
    "Type_Inspections_All" AS type_inspections_all,
    CAST("Avg_No_Routine" AS BIGINT) AS avg_no_routine,
    CAST("Avg_No_Reinspection" AS BIGINT) AS avg_no_reinspection,
    CAST("Announce_Inspec" AS BOOLEAN) AS announce_inspec,
    "Grading_Method_All" AS grading_method_all,
    CAST("Public_Disclosure" AS BOOLEAN) AS public_disclosure,
    "Disclosure_Method_All" AS disclosure_method_all,
    CAST("No_Outbreaks" AS BIGINT) AS no_outbreaks,
    CAST("No_Complaints" AS BIGINT) AS no_complaints,
    CAST("No_Salmonella" AS BIGINT) AS no_salmonella,
    CAST("No_Ecoli" AS BIGINT) AS no_ecoli
FROM "cdc-6zuv-bn3z"
