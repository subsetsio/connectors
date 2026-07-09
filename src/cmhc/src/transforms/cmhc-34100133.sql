-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `type_of_structure` categories are nested, not disjoint: 'Apartment structures of three units and over' contains 'Apartment structures of six units and over', and 'Row and apartment structures of three units and over' is the union of the row and apartment categories. Filter to one structure type; never sum across.
SELECT
    "REF_DATE" AS ref_date,
    "GEO" AS geo,
    "DGUID" AS dguid,
    "Type of structure" AS type_of_structure,
    "Type of unit" AS type_of_unit,
    "UOM" AS uom,
    "UOM_ID" AS uom_id,
    "SCALAR_FACTOR" AS scalar_factor,
    "SCALAR_ID" AS scalar_id,
    "VECTOR" AS vector,
    "COORDINATE" AS coordinate,
    "VALUE" AS value,
    "STATUS" AS status,
    "SYMBOL" AS symbol,
    "TERMINATED" AS terminated,
    "DECIMALS" AS decimals
FROM "cmhc-34100133"
