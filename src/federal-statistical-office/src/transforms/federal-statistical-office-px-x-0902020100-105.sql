-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("gebäudekategorie" AS VARCHAR) AS "gebäudekategorie",
    CAST("heizungsart" AS VARCHAR) AS "heizungsart",
    CAST("energieträger_der_heizung" AS VARCHAR) AS "energieträger_der_heizung",
    CAST("bauperiode" AS VARCHAR) AS "bauperiode",
    CAST("warmwasserversorgung" AS VARCHAR) AS "warmwasserversorgung",
    CAST("energieträger_für_warmwasser" AS VARCHAR) AS "energieträger_für_warmwasser",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0902020100-105"
