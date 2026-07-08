SELECT
        "bathingWaterIdentifier",
        "geographicalConstraint",
        "groupIdentifier",
        "link",
        CAST("metadata_beginLifeSpanVersion" AS TIMESTAMP) AS "metadata_beginLifeSpanVersion",
        CAST("metadata_endLifeSpanVersion" AS TIMESTAMP) AS "metadata_endLifeSpanVersion",
        "metadata_observationStatus",
        "metadata_replacedBy",
        "metadata_replaces",
        "metadata_statements",
        "metadata_statusCode",
        CAST("metadata_statusDate" AS TIMESTAMP) AS "metadata_statusDate",
        "metadata_versionId",
        "qualityClass",
        "remarks",
        "season",
        "UID"
    FROM "eea-bathing-water-timeseries-characterisation"
