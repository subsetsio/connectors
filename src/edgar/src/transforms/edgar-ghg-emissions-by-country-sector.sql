-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include sector-level emissions and EDGAR country or regional aggregates; filter the geography and IPCC sector level deliberately before summing.
-- caution: The `gas` column mixes CH4, N2O, CO2bio, and individual fluorinated-gas species, all reported in kilotonnes of the named substance rather than CO2-equivalent.
SELECT
    "country_code",
    "country_name",
    "ipcc_annex",
    "c_group",
    "ipcc_sector_code",
    "ipcc_sector_name",
    "gas",
    "fossil_bio",
    "year",
    "emissions_kt"
FROM "edgar-ghg-emissions-by-country-sector"
