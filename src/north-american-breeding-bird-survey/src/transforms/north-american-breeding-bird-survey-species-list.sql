SELECT
    TRY_CAST(TRIM(Seq) AS INTEGER) AS seq,
    TRY_CAST(TRIM(AOU) AS INTEGER) AS aou,
    TRIM(English_Common_Name)      AS english_common_name,
    TRIM(French_Common_Name)       AS french_common_name,
    TRIM("Order")                  AS "order",
    TRIM(Family)                   AS family,
    TRIM(Genus)                    AS genus,
    TRIM(Species)                  AS species
FROM "north-american-breeding-bird-survey-species-list"
