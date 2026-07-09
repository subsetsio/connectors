-- caution: `geo_unit` mixes countries with regional aggregates (see the geounits dimension, `type` = REGIONAL) — summing across geo_unit double-counts.
-- caution: Indicators are heterogeneous: values carry no unit column, so rows are only comparable within one `indicator_id`. Never aggregate `value` across indicators.
-- caution: `qualifier` and `magnitude` flag observations UIS annotates (e.g. estimated, national estimate) — a null qualifier does not certify an unflagged observation.
-- The raw fact carries only codes. Both codebooks are deps of this node and are
-- joined on their verified unique keys, so the join cannot change the grain; the
-- codes stay beside the labels as provenance.
SELECT
    v."indicator_id",
    i."name"                     AS indicator_name,
    i."theme"                    AS theme,
    v."geo_unit",
    g."name"                     AS geo_unit_name,
    g."type"                     AS geo_unit_type,
    v."year",
    v."value",
    v."magnitude",
    v."qualifier"
FROM "unesco-institute-for-statistics-values" v
LEFT JOIN "unesco-institute-for-statistics-indicators" i
       ON v."indicator_id" = i."indicator_code"
LEFT JOIN "unesco-institute-for-statistics-geounits" g
       ON v."geo_unit" = g."id"
WHERE v."value" IS NOT NULL
