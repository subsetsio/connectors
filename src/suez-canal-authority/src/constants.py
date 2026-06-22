"""Static catalog data for the suez-canal-authority connector.

ENTITY_IDS is the rank-accepted entity union (copied from
data/sources/suez-canal-authority/work/entity_union.json). REPORT_KEYS maps each
entity id to the anonymous Power BI "publish to web" resource key (the 'k' GUID
decoded from each app.powerbi.com/view?r=<base64> embed link on the SCA
Navigation Statistics page). Everything else a fetch needs — modelId, datasetId,
reportId, entity name, columns — is discovered live from the resource key, so
this mapping is the only per-report data that has to be pinned here.
"""

ENTITY_IDS = [
    "01-monthly-number-net-ton-by-ship-type",
    "02-fiscal-year-statistical",
    "03-yearly-statistics",
    "04-yearly-cargo-ton-by-direction",
    "05-yealy-cargo-ton-by-region",
    "06-yealy-cargo-ton-by-region-cont",
    "07-yearly-cargo-ton-by-cargo-type",
]

REPORT_KEYS = {
    "01-monthly-number-net-ton-by-ship-type": "37989a27-9212-47b5-af4a-4e24459656ce",
    "02-fiscal-year-statistical": "cfd839a0-d4ac-4df7-a6e7-308bf576098b",
    "03-yearly-statistics": "173bc878-0a20-4bc1-b738-08d2de20719e",
    "04-yearly-cargo-ton-by-direction": "a9b8cc80-3266-4a27-bb9d-50ccb99ba5d6",
    "05-yealy-cargo-ton-by-region": "f394fa83-f56e-4ff5-8877-a2c015ca9cfe",
    "06-yealy-cargo-ton-by-region-cont": "620624d7-ba78-4a4b-a04a-3bb4d7f69b95",
    "07-yearly-cargo-ton-by-cargo-type": "4421f780-4bb4-47ac-8e7d-aba8b30360e6",
}
