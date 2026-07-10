-- Passthrough placeholder. The E3WebApp layer schema could not be profiled at
-- authoring time (GeoServer host unreachable from this egress), so the raw
-- columns are preserved verbatim as VARCHAR. The model stage recompiles this
-- with proper casts once the raw is profiled (compile-transforms).
SELECT * FROM "global-volcanism-program-e3webapp-holocenevolcanoes"
