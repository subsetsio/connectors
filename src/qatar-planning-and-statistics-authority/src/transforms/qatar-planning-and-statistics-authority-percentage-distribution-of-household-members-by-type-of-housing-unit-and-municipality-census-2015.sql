-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "number_of_household_members_dd_frd_l_sr",
    "apartment_shq",
    "arabic_popular_elderly_house_byt_rby_byt_sh_by_byt_jz",
    "palace_villa_qsr_fyl",
    "part_of_unit_bldg_jz_mn_whd_mbn",
    "others_khr",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-percentage-distribution-of-household-members-by-type-of-housing-unit-and-municipality-census-2015"
