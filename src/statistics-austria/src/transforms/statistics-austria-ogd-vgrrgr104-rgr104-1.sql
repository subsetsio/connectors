-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "nuts_3",
    "gross_regional_product_current_prices_in_million_euro",
    "gross_regional_product_per_inhabitant",
    "gross_regional_product_per_person_employed",
    "change_in_to_previous_year_prices",
    "ver_nderung_des_brp_pro_kopf_auf_basis_von_vorjahrespreisen_in"
FROM "statistics-austria-ogd-vgrrgr104-rgr104-1"
