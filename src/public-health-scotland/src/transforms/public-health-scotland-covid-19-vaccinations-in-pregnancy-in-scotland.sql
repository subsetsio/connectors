-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Country" AS country,
    strptime("WeekEnding", '%Y%m%d')::DATE AS weekending,
    "Dose" AS dose,
    "DoseQF" AS doseqf,
    CAST("NumberVaccinated" AS BIGINT) AS numbervaccinated,
    CAST("Month" AS BIGINT) AS month,
    "StageOfPregnancy" AS stageofpregnancy,
    "StageOfPregnancyQF" AS stageofpregnancyqf,
    "Product" AS product,
    "ProductQF" AS productqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    CAST("NumberOfPregnancies" AS BIGINT) AS numberofpregnancies,
    CAST("PercentVaccinated" AS DOUBLE) AS percentvaccinated,
    "SIMDQuintile" AS simdquintile,
    "SIMDQuintileQF" AS simdquintileqf,
    CAST("NumberOfDeliveries" AS BIGINT) AS numberofdeliveries,
    CAST("NumberDeliveriesVaccinated" AS BIGINT) AS numberdeliveriesvaccinated,
    CAST("PcDeliveriesVaccinated" AS DOUBLE) AS pcdeliveriesvaccinated,
    CAST("NumberDeliveriesDoubleVaccinated" AS BIGINT) AS numberdeliveriesdoublevaccinated,
    CAST("PcDeliveriesDoubleVaccinated" AS DOUBLE) AS pcdeliveriesdoublevaccinated,
    "HB" AS hb,
    "HBQF" AS hbqf
FROM "public-health-scotland-covid-19-vaccinations-in-pregnancy-in-scotland"
