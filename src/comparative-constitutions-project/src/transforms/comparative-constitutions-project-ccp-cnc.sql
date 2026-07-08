SELECT * REPLACE (
    TRY_CAST(year AS INTEGER)    AS year,
    TRY_CAST(cowcode AS INTEGER) AS cowcode
)
FROM "comparative-constitutions-project-ccp-cnc"
