-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "service_territory",
    "majorincidents",
    "_4mto6mtraindelays" AS "4mto6mtraindelays",
    "avgdelayperlatetrain",
    "nooftrainsover15minslate",
    "noofshorttrains"
FROM "mta-open-data-sguy-yhj4"
