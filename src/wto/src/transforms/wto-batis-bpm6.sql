-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains reported, final, and balanced values for bilateral services flows; choose the appropriate value column before aggregating.
-- caution: Reporter and partner include economies and aggregate groupings, so filter entity type columns when country-only totals are required.
SELECT
    "Reporter" AS reporter,
    "type_Reporter" AS type_reporter,
    "Partner" AS partner,
    "type_Partner" AS type_partner,
    "Flow" AS flow,
    "Item_code" AS item_code,
    "type_Item" AS type_item,
    CAST("Year" AS BIGINT) AS year,
    TRY_CAST("Reported_value" AS DOUBLE) AS reported_value,
    CAST("Final_value" AS DOUBLE) AS final_value,
    "Final_value_methodology" AS final_value_methodology,
    CAST("Balanced_value" AS DOUBLE) AS balanced_value
FROM "wto-batis-bpm6"
