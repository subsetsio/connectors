# The entity union — the rank-active Bank of Finland open-data datasets.
# Copied from data/sources/bank-of-finland/work/entity_union.json. Data, not logic.
ENTITY_IDS = [
    "BOF_BKN1_PUBL",
    "BOF_BSI1_PUBL",
    "BOF_CSEC_PUBL",
    "BOF_CSEC_SHR_PUBL",
    "IVF_PUBL",
    "MFI_PUBL",
    "OFI_PUBL",
    "PAY_PUBL",
]

# Expected series count per dataset, observed during research (the v4
# /series/{ds} totalCount). Used by the per-node expectation tests as a
# degradation floor — a large shortfall means pagination/batching broke.
SERIES_COUNT = {
    "BOF_BKN1_PUBL": 14,
    "BOF_BSI1_PUBL": 67,
    "BOF_CSEC_PUBL": 432,
    "BOF_CSEC_SHR_PUBL": 44,
    "IVF_PUBL": 257,
    "MFI_PUBL": 1382,
    "OFI_PUBL": 269,
    "PAY_PUBL": 255,
}
