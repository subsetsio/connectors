-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Coefficient" AS coefficient,
    "Output_Total" AS output_total,
    "Output_Direct" AS output_direct,
    "Output_Indirect" AS output_indirect,
    "ValueAdded_Total" AS valueadded_total,
    "ValueAdded_Direct" AS valueadded_direct,
    "ValueAdded_Indirect" AS valueadded_indirect,
    "Imports_Total" AS imports_total,
    "Imports_Direct" AS imports_direct,
    "Imports_Indirect" AS imports_indirect
FROM "sg-data-d-6bf6e5ef1023e99fc1cf8c55006a386b"
