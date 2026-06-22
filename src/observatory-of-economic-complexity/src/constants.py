"""Per-cube extraction config for the OEC Tesseract OLAP API.

This is DATA, not logic: which OLAP cubes we publish and, per cube, the exact
drilldown levels + measures that define the published table's grain, plus an
ordered list of levels to partition by when a single query exceeds the server's
cell cap (HTTP 413).

Grain choices (the "why"):
- Many complexity cubes carry a parallel "<X> Rank" dimension that mirrors a
  primary dimension; drilling it would explode the table into a sparse
  cross-join. We drill only the real dimensions and let the engine aggregate
  the rank away (one row per primary x year).
- Bilateral trade/tariff cubes (BACI / Comtrade / WITS / WTO) are N^2 in
  countries x products x years and cannot be pulled whole. We publish the
  reporter/exporter side (product x reporter-country x time) — the standard
  "country trade profile" grain — dropping the partner/importer dimension to
  stay tractable. `bilateral_relatedness` is inherently bilateral so it keeps
  both country sides and is partitioned by exporter.
- `split_order` is the partition axis used adaptively: the fetcher tries the
  whole cube first and, on 413, recurses over the members of these levels (each
  must also appear in `drilldowns` so its value survives in the output).

Keys are the OEC cube names = the rank-accepted entity union (49 entities).
"""

# level lists kept short; "Official" levels are OEC's canonical labelled levels.
_ECI = {"drilldowns": ["Country Official", "Year"], "measures": ["ECI"], "split_order": ["Year"]}
_PCI4 = {"drilldowns": ["HS4 Official", "Year"], "measures": ["PCI"], "split_order": ["Year"]}
_PCI6 = {"drilldowns": ["HS6 Official", "Year"], "measures": ["PCI"], "split_order": ["Year"]}
# BACI: HS2 product grain, eagerly partitioned by Year so every request is small
# (~1.4 MB). The HS2-whole response is 43 MB and large responses stall under the
# source's throttling — small per-year requests are the reliable shape.
_BACI = {
    "drilldowns": ["HS2 Official", "Exporter Country Official", "Year"],
    "measures": ["Trade Value", "Quantity"],
    "split_order": ["Year", "Exporter Country Official"],
    "eager_split": True,
}

CUBES = {
    # --- Economic Complexity Index (country x year) ---
    "complexity_eci_a_hs02_hs4": _ECI,
    "complexity_eci_a_hs02_hs6": _ECI,
    "complexity_eci_a_hs07_hs4": _ECI,
    "complexity_eci_a_hs07_hs6": _ECI,
    "complexity_eci_a_hs12_hs4": _ECI,
    "complexity_eci_a_hs12_hs6": _ECI,
    "complexity_eci_a_hs17_hs4": _ECI,
    "complexity_eci_a_hs17_hs6": _ECI,
    "complexity_eci_a_hs22_hs4": _ECI,
    "complexity_eci_a_hs22_hs6": _ECI,
    "complexity_eci_a_hs92_hs4": _ECI,
    "complexity_eci_a_hs92_hs6": _ECI,
    "complexity_eci_a_hs96_hs4": _ECI,
    "complexity_eci_a_hs96_hs6": _ECI,
    "complexity_eci_multidimensional": {
        "drilldowns": ["Country Official", "Year"],
        "measures": ["ECI Research", "ECI Technology"],
        "split_order": ["Year"],
    },
    "complexity_eci_software": {
        "drilldowns": ["Country Official", "Year"],
        "measures": ["ECI Software"],
        "split_order": ["Year"],
    },
    # --- Product Complexity Index (product x year) ---
    "complexity_pci_a_hs02_hs4": _PCI4,
    "complexity_pci_a_hs07_hs4": _PCI4,
    "complexity_pci_a_hs12_hs4": _PCI4,
    "complexity_pci_a_hs17_hs4": _PCI4,
    "complexity_pci_a_hs22_hs4": _PCI4,
    "complexity_pci_a_hs92_hs4": _PCI4,
    "complexity_pci_a_hs96_hs4": _PCI4,
    "complexity_pci_a_hs02_hs6": _PCI6,
    "complexity_pci_a_hs07_hs6": _PCI6,
    "complexity_pci_a_hs12_hs6": _PCI6,
    "complexity_pci_a_hs17_hs6": _PCI6,
    "complexity_pci_a_hs22_hs6": _PCI6,
    "complexity_pci_a_hs92_hs6": _PCI6,
    "complexity_pci_a_hs96_hs6": _PCI6,
    # --- Inequality ---
    "gini_inequality_combined": {
        "drilldowns": ["Country Official", "Year"],
        "measures": ["Gini Coefficient (EHII)", "Gini Coefficient (World Bank)"],
        "split_order": ["Year"],
    },
    # --- World Development Indicators (country x indicator x year) ---
    "indicators_i_wdi_a": {
        "drilldowns": ["Country Official", "Indicator", "Year"],
        "measures": ["Measure"],
        "split_order": ["Country Official", "Indicator"],
    },
    # --- Services trade (reporter side) ---
    "services_i_comtrade_a_eb02": {
        "drilldowns": ["Trade Flow", "Reporter Country Official", "Service", "Year"],
        "measures": ["Service Value"],
        "split_order": ["Year", "Reporter Country Official"],
        "eager_split": True,
    },
    # --- Tariffs (HS2 product grain — fits in a single small request) ---
    "tariffs_i_wits_a_hs_new": {
        "drilldowns": ["Reporter Country Official", "HS2 Official", "Year"],
        "measures": ["Tariff"],
        "split_order": ["Year", "Reporter Country Official"],
    },
    "wto_tariffs": {
        "drilldowns": ["Reporter Country Official", "HS2 Official", "Year"],
        "measures": [
            "Avg AdValorem Tariff",
            "Maximum AdValorem Tariff",
            "Minimum AdValorem Tariff",
            "Number of AdValorem Tariff Lines",
        ],
        "split_order": ["Year", "Reporter Country Official"],
    },
    # --- BACI bilateral product trade (reporter/exporter side) ---
    "trade_i_baci_a_02": _BACI,
    "trade_i_baci_a_07": _BACI,
    "trade_i_baci_a_12": _BACI,
    "trade_i_baci_a_17": _BACI,
    "trade_i_baci_a_22": _BACI,
    "trade_i_baci_a_92": _BACI,
    "trade_i_baci_a_96": _BACI,
    # --- UN Comtrade (reporter side, HS2/SITC grain, year-partitioned) ---
    "trade_i_comtrade_a_hs92": {
        "drilldowns": ["Trade Flow", "Reporter Country Official", "HS2 Official", "Year"],
        "measures": ["Trade Value", "Quantity", "Weight"],
        "split_order": ["Year", "Reporter Country Official"],
    },
    "trade_i_comtrade_a_sitc2": {
        "drilldowns": ["Trade Flow", "Reporter Country Official", "Division", "Year"],
        "measures": ["Trade Value", "Quantity", "Weight"],
        "split_order": ["Year", "Reporter Country Official"],
    },
    "trade_i_comtrade_m_hs": {
        # monthly HS6 bilateral is far too large; publish at HS2 monthly grain.
        "drilldowns": ["Trade Flow", "Reporter Country Official", "HS2 Official", "Time"],
        "measures": ["Trade Value", "Net Weight"],
        "split_order": ["Time", "Reporter Country Official"],
    },
    # --- OEC SITC2 historical trade (exporter side) ---
    "trade_i_oec_a_sitc2": {
        "drilldowns": ["Exporter Country Official", "Division", "Year"],
        "measures": ["Trade Value", "Quantity", "Weight"],
        "split_order": ["Year", "Exporter Country Official"],
    },
    # --- Spain monthly product trade (single reporter) ---
    "trade_s_esp_m_hs": {
        "drilldowns": ["Trade Flow", "Product Official", "Time"],
        "measures": ["Trade Value", "Quantity", "Weight"],
        "split_order": ["Time", "Product Official"],
    },
    # --- Bilateral relatedness (keeps both country sides; HS2 grain,
    #     partitioned by exporter so each request is ~3.7 MB) ---
    "bilateral_relatedness": {
        "drilldowns": [
            "HS2 Official",
            "Exporter Country Official",
            "Importer Country Official",
            "Year",
        ],
        "measures": [
            "PCI",
            "Trade Value",
            "ECI Exporter",
            "ECI Importer",
            "RCA Exporter",
            "RCA Importer",
        ],
        "split_order": ["Exporter Country Official", "Importer Country Official"],
        "eager_split": True,
    },
    # --- SEC 13F institutional manager filings ---
    "13f_managers": {
        "drilldowns": ["Report Period Date", "Central Key Index", "Filing Manager Name"],
        "measures": ["Market Value", "Holdings"],
        "split_order": ["Report Period Date"],
    },
}

# The entity union (rank-accepted) is exactly the CUBES keys.
ENTITY_IDS = list(CUBES.keys())
