-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Presentation asset: SVG path geometry and label anchors for rendering French département/région maps, in an unspecified local drawing space — not a georeferenced coordinate system, and not usable for spatial joins.
-- caution: `filename` splits the same territory across map panels (metropolitan France, Île-de-France inset, each overseas territory), so a territory `id` appears in more than one row.
SELECT
    "d",
    CAST("data_anchor_x" AS DOUBLE) AS data_anchor_x,
    CAST("data_anchor_y" AS DOUBLE) AS data_anchor_y,
    "data_fill_id",
    "data_name",
    "id",
    "filename",
    "niveau",
    "cle"
FROM "cnam-georef-svg0"
