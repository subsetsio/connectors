-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table combines several merchandise value indicators and product/category levels; filter indicator and product fields before aggregating.
-- caution: Reporter and partner fields include aggregate groupings alongside economies.
SELECT
    "IndicatorCategory" AS indicatorcategory,
    "IndicatorCode" AS indicatorcode,
    "Indicator" AS indicator,
    "ReporterCode" AS reportercode,
    "ReporterISO3A" AS reporteriso3a,
    "Reporter" AS reporter,
    "PartnerCode" AS partnercode,
    "PartnerISO3A" AS partneriso3a,
    "Partner" AS partner,
    "ProductClassificationCode" AS productclassificationcode,
    "ProductClassification" AS productclassification,
    "ProductCode" AS productcode,
    "Product" AS product,
    "PeriodCode" AS periodcode,
    "Period" AS period,
    "FrequencyCode" AS frequencycode,
    "Frequency" AS frequency,
    "UnitCode" AS unitcode,
    "Unit" AS unit,
    CAST("Year" AS BIGINT) AS year,
    "ValueFlagCode" AS valueflagcode,
    "ValueFlag" AS valueflag,
    CAST("Value" AS DOUBLE) AS value
FROM "wto-merchandise-values-annual"
