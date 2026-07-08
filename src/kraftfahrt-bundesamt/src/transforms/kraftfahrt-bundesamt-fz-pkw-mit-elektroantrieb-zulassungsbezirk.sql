SELECT COLUMNS(c -> NOT regexp_matches(lower(c), '^(objectid|object_id|oid|fid|shape__|monat_sortierung)')) FROM "kraftfahrt-bundesamt-fz-pkw-mit-elektroantrieb-zulassungsbezirk"
