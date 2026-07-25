-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "country",
    CAST("year" AS BIGINT) AS year,
    CAST("inbound_international" AS BIGINT) AS inbound_international,
    CAST("inbound_international_1" AS BIGINT) AS inbound_international_1,
    CAST("inbound_international_seats" AS BIGINT) AS inbound_international_seats,
    CAST("inbound_international_load" AS DOUBLE) AS inbound_international_load,
    CAST("inbound_international_2" AS BIGINT) AS inbound_international_2,
    CAST("inbound_international_seats_1" AS BIGINT) AS inbound_international_seats_1,
    CAST("inbound_international_distance" AS BIGINT) AS inbound_international_distance,
    CAST("inbound_international_distance_1" AS BIGINT) AS inbound_international_distance_1,
    CAST("inbound_international_payload" AS BIGINT) AS inbound_international_payload,
    CAST("inbound_international_freight" AS BIGINT) AS inbound_international_freight,
    CAST("inbound_international_mail" AS BIGINT) AS inbound_international_mail,
    CAST("outbound_international" AS BIGINT) AS outbound_international,
    CAST("outbound_international_1" AS BIGINT) AS outbound_international_1,
    CAST("outbound_international_seats" AS BIGINT) AS outbound_international_seats,
    CAST("outbound_international_load" AS DOUBLE) AS outbound_international_load,
    CAST("outbound_international_2" AS DOUBLE) AS outbound_international_2,
    CAST("outbound_international_seats_1" AS BIGINT) AS outbound_international_seats_1,
    CAST("outbound_international_3" AS BIGINT) AS outbound_international_3,
    CAST("outbound_international_4" AS BIGINT) AS outbound_international_4,
    CAST("outbound_international_payload" AS BIGINT) AS outbound_international_payload,
    CAST("outbound_international_freight" AS BIGINT) AS outbound_international_freight,
    CAST("outbound_international_mail" AS BIGINT) AS outbound_international_mail,
    "country_name"
FROM "u-s-department-of-transportation-56rv-9p75"
