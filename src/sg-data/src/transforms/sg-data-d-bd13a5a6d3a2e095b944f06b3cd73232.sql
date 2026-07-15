-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "UniqueId" AS uniqueid,
    "Letter" AS letter,
    "Group" AS group,
    "IntraGroupOrdering" AS intragroupordering,
    "EntityName" AS entityname,
    "Description" AS description,
    "ContactMethodsStringified" AS contactmethodsstringified,
    "OtherInformation" AS otherinformation
FROM "sg-data-d-bd13a5a6d3a2e095b944f06b3cd73232"
