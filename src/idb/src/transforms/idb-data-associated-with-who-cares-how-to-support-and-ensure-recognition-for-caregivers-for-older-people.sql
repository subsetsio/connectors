-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pais" AS pais,
    "Dentro_del_hogar_miles" AS dentro_del_hogar_miles,
    "Fuera_del_hogar_imles" AS fuera_del_hogar_imles,
    "Total_miles" AS total_miles,
    "source_resource"
FROM "idb-data-associated-with-who-cares-how-to-support-and-ensure-recognition-for-caregivers-for-older-people"
