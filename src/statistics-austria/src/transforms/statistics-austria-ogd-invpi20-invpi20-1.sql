-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "c_manufactured_products",
    "domestic_goods",
    "imported_goods",
    "c_13_textiles",
    "c_22_rubber_and_plastic_products",
    "c_23_other_non_metallicmineral_products",
    "c_25_fabricated_metal_products_except_machinery_and_equipment",
    "c_26_computer_electronic_and_optical_products",
    "c_27_electrical_equipment",
    "c_28_machinery_and_equipment_n_e_c",
    "c_29_motor_vehicles_trailers_and_semi_trailers",
    "c_30_other_transport_equipment",
    "c_31_furniture",
    "c_32_other_manufactured_goods"
FROM "statistics-austria-ogd-invpi20-invpi20-1"
