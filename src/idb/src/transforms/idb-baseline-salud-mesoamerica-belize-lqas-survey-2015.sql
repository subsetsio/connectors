-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SM2015_BLZ_LQAS_en_Data_Dictionary" AS sm2015_blz_lqas_en_data_dictionary,
    "Unnamed:_1" AS data_dictionary_column_1,
    "Unnamed:_2" AS data_dictionary_column_2,
    "Unnamed:_3" AS data_dictionary_column_3,
    "Unnamed:_4" AS data_dictionary_column_4,
    "source_resource"
FROM "idb-baseline-salud-mesoamerica-belize-lqas-survey-2015"
