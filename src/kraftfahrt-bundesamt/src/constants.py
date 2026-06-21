"""Catalog data for the KBA Statistikportal connector.

ENTITY_IDS / SERVICES are the entity union (rank-accepted subsets) and the
slug -> ArcGIS FeatureServer-layer URL map, both copied verbatim from the
Hub DCAT feed at collect time. Data, not logic: kept out of the node module.
"""

ENTITY_IDS = [
    "fz-fahrzeugdichte",
    "fz-hersteller-handelsnamen-kfz",
    "fz-hersteller-handelsnamen-krad",
    "fz-hersteller-handelsnamen-nfz",
    "fz-hersteller-handelsnamen-pkw",
    "fz-modellreihen",
    "fz-modellreihen-bestand",
    "fz-pkw-mit-elektro-antrieb-gitterzellen",
    "fz-pkw-mit-elektro-antrieb-regionen",
    "fz-pkw-mit-elektro-antrieb-regiostar",
    "fz-pkw-mit-elektroantrieb-bundesland",
    "fz-pkw-mit-elektroantrieb-gemeinde",
    "fz-pkw-mit-elektroantrieb-zulassungsbezirk",
    "fz-top3modellreihensegment",
    "fz-top3modellreihensegment-bestand",
    "fz-top50modellreihen",
    "fz-top50modellreihen-bestand",
    "kf-verkehrsauff-lligkeiten",
    "vd-g-terverkehrsflotte",
    "ve-g-terbef-rderung-ausfahrten",
    "ve-g-terbef-rderung-einfahrten",
    "ve-gueterbefoerderung-top10",
]

# slug -> ArcGIS hosted FeatureServer layer 0 (query endpoint base)
SERVICES = {
    "fz-fahrzeugdichte": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/Fahrzeugdichte_gesamt/FeatureServer/0",
    "fz-hersteller-handelsnamen-kfz": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/SP_HSN_TSN_92a1e/FeatureServer/0",
    "fz-hersteller-handelsnamen-krad": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/SP_Hersteller_Handelsnamen_Krad_f73ec/FeatureServer/0",
    "fz-hersteller-handelsnamen-nfz": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/SP_Hersteller_Handelsnamen_NFZ_918d9/FeatureServer/0",
    "fz-hersteller-handelsnamen-pkw": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/SP_Hersteller_Handelsnamen_PKW_5c784/FeatureServer/0",
    "fz-modellreihen": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/SP_Modellreihen/FeatureServer/0",
    "fz-modellreihen-bestand": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ_Modellreihen_Bestand/FeatureServer/0",
    "fz-pkw-mit-elektro-antrieb-gitterzellen": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ_Pkw_mit_Elektro_Antrieb_Gitterzellen/FeatureServer/0",
    "fz-pkw-mit-elektro-antrieb-regionen": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ%20Pkw%20mit%20Elektro%20Antrieb%20Regionen/FeatureServer/0",
    "fz-pkw-mit-elektro-antrieb-regiostar": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ_Pkw_mit_Elektro_Antrieb_RegioStaR/FeatureServer/19",
    "fz-pkw-mit-elektroantrieb-bundesland": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ%20Pkw%20mit%20Elektroantrieb%20Bundesland/FeatureServer/0",
    "fz-pkw-mit-elektroantrieb-gemeinde": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ%20Pkw%20mit%20Elektroantrieb%20Gemeinde/FeatureServer/0",
    "fz-pkw-mit-elektroantrieb-zulassungsbezirk": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ%20Pkw%20mit%20Elektroantrieb%20Zulassungsbezirk/FeatureServer/0",
    "fz-top3modellreihensegment": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/Top3ModellreihenSegment_aktuell/FeatureServer/0",
    "fz-top3modellreihensegment-bestand": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ_Top3ModellreihenSegment_Bestand/FeatureServer/0",
    "fz-top50modellreihen": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/Top50Modellreihen_aktuell/FeatureServer/0",
    "fz-top50modellreihen-bestand": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/FZ_Top50Modellreihen_Bestand/FeatureServer/0",
    "kf-verkehrsauff-lligkeiten": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/VA_Layer/FeatureServer/0",
    "vd-g-terverkehrsflotte": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/VD_Layer/FeatureServer/0",
    "ve-g-terbef-rderung-ausfahrten": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/VE_G%C3%BCterbef%C3%B6rderung_Ausfahrten/FeatureServer/0",
    "ve-g-terbef-rderung-einfahrten": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/VE_G%C3%BCterbef%C3%B6rderung_Einfahrten/FeatureServer/0",
    "ve-gueterbefoerderung-top10": "https://services-eu1.arcgis.com/U09msXRZoxesNntH/arcgis/rest/services/VE_Gueterbefoerderung_Top10/FeatureServer/0",
}
