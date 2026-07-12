-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sink_category",
    "greenhouse_gas_source",
    "msdr_gzt_lhtbs_lhrry",
    "emissions_of_sulfur_dioxide_so2",
    "emissions_of_non_methane_volatile_organic_compounds_nm_vocs",
    "emissions_of_co",
    "emissions_of_nitrogen_oxides_nox",
    "emissions_of_nitrous_oxide_n2o",
    "emissions_of_methane_ch4",
    "emissions_of_carbon_dioxide_co2"
FROM "qatar-planning-and-statistics-authority-sectoral-report-for-national-greenhouse-gas-inventories-for-industrial-processes"
