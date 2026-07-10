-- Placeholder passthrough. The E3WebApp layer schema could not be profiled at
-- authoring time (the GeoServer host was unreachable from this egress), so this
-- publishes only the four base E3WebApp columns (present on the sibling
-- E3WebApp_Emissions layer). The model stage recompiles this with the full
-- profiled schema + casts once the raw is observed (compile-transforms).
SELECT
    FID,
    VolcanoName,
    VolcanoNumber,
    GeoLocation
FROM "global-volcanism-program-e3webapp-holocenevolcanoes"
