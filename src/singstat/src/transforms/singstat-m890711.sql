-- faithful pass-through of flattened SingStat Table Builder raw asset `singstat-m890711`.
-- Regenerate from the model stage after the first successful full run.
SELECT
    "period",
    "series_no",
    "series_text",
    "uom",
    "value"
FROM "singstat-m890711"
