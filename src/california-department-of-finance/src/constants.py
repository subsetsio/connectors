# Entity union for california-department-of-finance — the rank-active ArcGIS
# item ids (DRU Demographic Research Unit hosted feature services / tables).
# Copied from data/sources/california-department-of-finance/work/entity_union.json.
# These are ArcGIS Online item ids (32-char lowercase hex, no underscores), so the
# NodeSpec id form f"{slug}-{eid.lower().replace('_','-')}" leaves them unchanged.
ENTITY_IDS = [
    "045273ed28ce4589be48edc75c611116",
    "060863044a0f4e4b8eec84c85e3eedf6",
    "0a50d4048b27441a84e8ff98e71d023e",
    "0e752a67c9d342599cd12f9ca15bceca",
    "0f200a12da104da3936bbf291b394fbc",
    "0f2f9e220e3b4ebc890e2a178560e574",
    "11fd91ff08f04c618b2f87bec2a1a420",
    "163d99a832d94a229e41c62dde35f96f",
    "1d0d7998ab75485f82d61e544df8b5ab",
    "2d99024a65fc49a2833b1222da48cc02",
    "397650f2bdfe40a7babffbcae91ae639",
    "4159d767e6894cb3ab7a991240ac3c18",
    "4633459306884884ac7f9036404cc0d1",
    "46bb74eb6829474681a69039144fe3e8",
    "4c2eb24715614327bd8b30f630234ef0",
    "4cda2d48228c4eea9571b69c493d8008",
    "4e4a998fa9c340d5804fd41f0b3a35bc",
    "4fa3ff8b968d481f8cb9799b07086ca2",
    "50a042556345443ab45d84716fadc43e",
    "5b4a50c56d414167b709e3fa93829063",
    "5f96af5d88634040a5018eedde7873f7",
    "603566ca1e3041c699fe924a12dc6f1b",
    "6b93d3b1a4b841f586f07406eb621b62",
    "7a040ca9fc594092aa86da996036095e",
    "837b17801b354716a83f22add1f7bf74",
    "99aec3eef9cc4ea79d2f5cefa13ff2ee",
    "a4f06236245e43409344f2eb3dc94340",
    "b7ddd718bd2a4292810896c37df07aa8",
    "b81dbe1dc5b64be38f75be06936aef14",
    "bc1cfb5ef50a43a9b60e25c11c32255b",
    "bc29bf11bdba43f0a813097e3f4a48a5",
    "cf497bb810394c9cb62e3b59021df371",
    "cf9ee3a2956f4958b5eca26805717ce1",
    "d4e959fd082a417295f594b61d577744",
    "d604f91a049a42d0bb7cabf17fdde9ff",
    "e27cb8246ca14b5d830083689b7c6f46",
    "e5a53914c12b42a9803885f69c26ca1f",
    "ee6b2c4f8fdb40edad85e682490509b9",
    "f38e6e7f9e1d47deafb032a9cd73cdd8",
    "f3e56cb333394a9aba52f7f911197212",
    # 2026-07-26 recollect: DRU rolled the wildfire housing-loss series to a
    # 2015-25 vintage under NEW item ids (plus related jurisdiction/popup
    # layers). The 2014-24 vintage items above remain live upstream and stay
    # published; these are additive, not replacements.
    "02325c8c06e04781b030c0a47ddf2a78",  # 2015-25 Wildfire Housing Loss County (All)
    "164e8cc7a4ea4eb3937739d591b3bbb1",  # Wildfire Impacts on CA Housing Stock by State/County/Subcounty 2015-2025
    "275e192ffded43f680bd40443bb5b73c",  # Top Counties Wildfire Related Housing Destruction
    "34fd73a6bb3547fb9f8ece6872d11dce",  # 2015-25 Wildfire Housing Loss Jurisdiction
    "796ce7a8b9bc48e5b4f8c51df6b2d914",  # City and State Wildfire-Related Housing Losses 2015-2025 (DINS)
    "95a31702222a4521a6c12cbd11e42fbe",  # California Area Boundaries
    "a5040e07601041469d058362e6d03f4e",  # jurisdiction popup
    "c2e9450604fa4b1d8a26729e3365962f",  # county popup
    "d05e060df7444647aa8e42c2982f951e",  # Top Ten Most Destructive Wildfires 2015-2025
    "d546228bac8d4819b235b0e4b92c3300",  # Summary of CA Wildfire-Related Housing Loss by Jurisdiction 2015-25
    "ef1f67a489714037a0c393d0300bf4b3",  # Wildfire Housing Loss from 2015-25 (Unincorporated)
    "f49d2d7e35fe47f9aac2fc20e5c0ca43",  # 2015-25 Wildfire Housing Loss (Sum All)
]
