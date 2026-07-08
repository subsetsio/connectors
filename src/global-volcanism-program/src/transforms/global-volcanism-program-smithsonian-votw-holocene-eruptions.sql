SELECT
    * EXCLUDE (
        Volcano_Number, Eruption_Number, ExplosivityIndexMax,
        StartDateYear, StartDateYearUncertainty, StartDateMonth, StartDateDay,
        StartDateDayUncertainty, EndDateYear, EndDateYearUncertainty,
        EndDateMonth, EndDateDay, EndDateDayUncertainty
    ),
    TRY_CAST(Volcano_Number AS BIGINT)            AS Volcano_Number,
    TRY_CAST(Eruption_Number AS BIGINT)           AS Eruption_Number,
    TRY_CAST(ExplosivityIndexMax AS INTEGER)      AS ExplosivityIndexMax,
    TRY_CAST(StartDateYear AS INTEGER)            AS StartDateYear,
    TRY_CAST(StartDateYearUncertainty AS INTEGER) AS StartDateYearUncertainty,
    TRY_CAST(StartDateMonth AS INTEGER)           AS StartDateMonth,
    TRY_CAST(StartDateDay AS INTEGER)             AS StartDateDay,
    TRY_CAST(StartDateDayUncertainty AS INTEGER)  AS StartDateDayUncertainty,
    TRY_CAST(EndDateYear AS INTEGER)              AS EndDateYear,
    TRY_CAST(EndDateYearUncertainty AS INTEGER)   AS EndDateYearUncertainty,
    TRY_CAST(EndDateMonth AS INTEGER)             AS EndDateMonth,
    TRY_CAST(EndDateDay AS INTEGER)               AS EndDateDay,
    TRY_CAST(EndDateDayUncertainty AS INTEGER)    AS EndDateDayUncertainty
FROM "global-volcanism-program-smithsonian-votw-holocene-eruptions"
