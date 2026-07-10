-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "FIRST_NAME" AS first_name,
    "LAST_NAME" AS last_name,
    "STATE" AS state,
    "ASM_COHORT" AS asm_cohort,
    "ORGANIZATION_LEGAL_NAME" AS organization_legal_name,
    "ASM_CY27_PARTICIPANT" AS asm_cy27_participant,
    "ASM_CY27_SMALLPRACTICE" AS asm_cy27_smallpractice,
    "ASM_CY28_PARTICIPANT" AS asm_cy28_participant,
    "ASM_CY28_SMALLPRACTICE" AS asm_cy28_smallpractice,
    "ASM_CY29_PARTICIPANT" AS asm_cy29_participant,
    "ASM_CY29_SMALLPRACTICE" AS asm_cy29_smallpractice,
    "ASM_CY30_PARTICIPANT" AS asm_cy30_participant,
    "ASM_CY30_SMALLPRACTICE" AS asm_cy30_smallpractice,
    "ASM_CY31_PARTICIPANT" AS asm_cy31_participant,
    "ASM_CY31_SMALLPRACTICE" AS asm_cy31_smallpractice
FROM "cms-175d576d-0568-4ac2-aec5-d77f3ee02205"
