-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Name" AS name,
    "WildfireAcres" AS wildfireacres,
    "FireCode" AS firecode,
    "IrwinID" AS irwinid,
    "FireDiscoveryDate" AS firediscoverydate,
    "ContainmentDate" AS containmentdate,
    "IgnitionFiscalYear" AS ignitionfiscalyear,
    "ID" AS id,
    "SourceSystemID" AS sourcesystemid,
    "SourceSystemName" AS sourcesystemname,
    "DiscoveryDate" AS discoverydate,
    "ContainDate" AS containdate,
    "CreatedOnDate" AS createdondate,
    "LastModifiedDate" AS lastmodifieddate,
    "GlobalID" AS globalid,
    "OBJECTID" AS objectid,
    "FireName" AS firename,
    "EntityType" AS entitytype,
    "Notes" AS notes,
    "IsFirePerimeter" AS isfireperimeter,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-3"
