-- Published pass-through of raw asset `cnam-georef-svg0`.
-- anchor coordinates stay VARCHAR: they are drawing-space numbers the source ships as strings, and two of them carry the row identity.
SELECT
    "filename" AS map_panel,
    "niveau" AS level,
    "cle" AS map_key,
    "id" AS territory_code,
    "data_fill_id" AS fill_id,
    "data_name" AS territory_name,
    "d" AS svg_path,
    "data_anchor_x" AS label_anchor_x,
    "data_anchor_y" AS label_anchor_y
FROM "cnam-georef-svg0"
