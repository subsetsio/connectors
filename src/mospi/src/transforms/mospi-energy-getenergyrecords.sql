-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `energy_sub_commodities` / `end_use_sub_sector` are NULL on the commodity- and sector-level totals that coexist with the detail rows.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "year",
    "indicator",
    "use_of_energy_balance",
    "energy_commodities",
    "energy_sub_commodities",
    "end_use_sector",
    "end_use_sub_sector",
    CAST("value" AS DOUBLE) AS value
FROM "mospi-energy-getenergyrecords"
