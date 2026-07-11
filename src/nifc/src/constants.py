"""Entity -> ArcGIS layer resolution for the NIFC connector.

Generated at build time by resolving each accepted `<itemid>-<layer>` entity
(the accept-stage entity union) to its live ArcGIS Feature Service URL via the
ArcGIS sharing content API. `url` is the FeatureServer service; `layer` is the
sublayer index queried at `<url>/<layer>/query`. All 94 are Feature Services in
the NIFC org (T4QMspbfLg3qTGWY) or the Esri Living-Atlas orgs (MODIS/VIIRS).
"""

LAYERS = {
    '003d6c8ad1624132aa43815ab7b74ba9-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2000/FeatureServer', "layer": 0},  # Historic Perimeters 2000
    '13dc2b7882f645009731442e42a3ffd2-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2003/FeatureServer', "layer": 0},  # Historic Perimeters 2003
    '20c1f27e9db94bc2a2ae1b183e4620d6-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/IMSR_Incident_Locations_Most_Recent_View/FeatureServer', "layer": 0},  # IMSR Incident Locations View: Current
    '265b3589ea664bca9d36f8171357b25c-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/DMP_JurisdictionalUnits_Public/FeatureServer', "layer": 0},  # Jurisdictional Units Public
    '2827d083ddc14464a8eab3181e8bf13e-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/2019_NIFS_OpenData/FeatureServer', "layer": 0},  # EventLine2019
    '2827d083ddc14464a8eab3181e8bf13e-1': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/2019_NIFS_OpenData/FeatureServer', "layer": 1},  # EventPoint2019
    '2827d083ddc14464a8eab3181e8bf13e-2': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/2019_NIFS_OpenData/FeatureServer', "layer": 2},  # EventPolygon2019
    '29185087b4594a35abe059cbdbf97ee4-1': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/PublicView_RAWS/FeatureServer', "layer": 1},  # Public View - Interagency Remote Automatic Weather Stations (RAWS)
    '2aa165c74bf040f1a44c63b505f1a940-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Incident_Feature_Service_2018/FeatureServer', "layer": 0},  # EventPoint2018
    '2aa165c74bf040f1a44c63b505f1a940-1': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Incident_Feature_Service_2018/FeatureServer', "layer": 1},  # EventLine2018
    '2aa165c74bf040f1a44c63b505f1a940-2': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Incident_Feature_Service_2018/FeatureServer', "layer": 2},  # EventPolygon2018
    '405814902c9e411cb4384c49d694e82b-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Incident_Locations_YearToDate/FeatureServer', "layer": 0},  # 2026 Wildland Fire Incident Locations to Date
    '4181a117dc9e43db8598533e29972015-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Incident_Locations_Current/FeatureServer', "layer": 0},  # Current Wildland Fire Incident Locations
    '45bd8a9c16b94a6a8e837c82b9a05226-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/DMP_National_IA_Frequency_Zones_Federal_Public/FeatureServer', "layer": 0},  # National IA Frequency Zones Federal Public
    '45ff876436e34182aee63f3ac352fb8b-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/DMP_Predictive_Service_Area__PSA_Boundaries_Public/FeatureServer', "layer": 0},  # Predictive Service Area  (PSA) Boundaries Public
    '4652a92ab9a64ad0816eb15b4b599db2-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2006/FeatureServer', "layer": 0},  # Historic Perimeters 2006
    '5c5cdca154e84eb39b022a6b9ebb31ff-3': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2023/FeatureServer', "layer": 3},  # Event Point
    '5c5cdca154e84eb39b022a6b9ebb31ff-5': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2023/FeatureServer', "layer": 5},  # Event Line
    '5c5cdca154e84eb39b022a6b9ebb31ff-6': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2023/FeatureServer', "layer": 6},  # Perimeter Line
    '5c5cdca154e84eb39b022a6b9ebb31ff-7': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2023/FeatureServer', "layer": 7},  # Event Polygon
    '5e72b1699bf74eefb3f3aff6f4ba5511-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters/FeatureServer', "layer": 0},  # WFIGS Interagency Fire Perimeters
    '60a94840152b4a89bec467a9f052f135-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/InFORM_FireOccurrence_Public/FeatureServer', "layer": 0},  # InFORM Fire Occurrence Data Records
    '614ad98bdf834c92bf92c4f0fe197903-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/DMP_NationalGACCBoundaries_Public/FeatureServer', "layer": 0},  # National GACC Boundaries Public
    '671f7337371d430baad822d017cfef87-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2010/FeatureServer', "layer": 0},  # Historic Perimeters 2010
    '674964c20aaa4e58814f6438c8e08d3a-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2017/FeatureServer', "layer": 0},  # Historic Perimeters 2017
    '696c45c4ecd34948b1ae87d2f567e347-3': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2022/FeatureServer', "layer": 3},  # EventPoint2022
    '696c45c4ecd34948b1ae87d2f567e347-5': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2022/FeatureServer', "layer": 5},  # EventLine2022
    '696c45c4ecd34948b1ae87d2f567e347-6': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2022/FeatureServer', "layer": 6},  # PerimeterLine2022
    '696c45c4ecd34948b1ae87d2f567e347-7': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2022/FeatureServer', "layer": 7},  # EventPolygon2022
    '6bb597e8bc1f49bfb68867b7b043adf0-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/DMP_National_IA_Frequency_Zones_International_Public/FeatureServer', "layer": 0},  # National IA Frequency Zones International Public
    '705b14551df6417aaea99dd7a651d9ff-2': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2024/FeatureServer', "layer": 2},  # Event Point
    '705b14551df6417aaea99dd7a651d9ff-4': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2024/FeatureServer', "layer": 4},  # Event Line
    '705b14551df6417aaea99dd7a651d9ff-5': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2024/FeatureServer', "layer": 5},  # Perimeter Line
    '705b14551df6417aaea99dd7a651d9ff-6': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2024/FeatureServer', "layer": 6},  # Event Polygon
    '78a4e0e43404408ab08bf84baa4528d8-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/DMP_National_Dispatch_Boundaries_Public/FeatureServer', "layer": 0},  # National Dispatch Boundaries Public
    '7c1b4059cc6c441297d7d2b3573cb337-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2016/FeatureServer', "layer": 0},  # Historic Perimeters 2016
    '7c81ab78d8464e5c9771e49b64e834e9-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_YearToDate/FeatureServer', "layer": 0},  # WFIGS 2026 Interagency Fire Perimeters to Date
    '8339e1f9499242279e922b43767b583d-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2015/FeatureServer', "layer": 0},  # Historic Perimeters 2015
    '85d3f50b5eee4dcfa48f5e4fb23aa9e1-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/IMSR_Incident_Locations_View_Occurrence_Last_Only_YTD/FeatureServer', "layer": 0},  # IMSR Incident Locations View: Final Occurrence Year-to-Date
    '862c7f33407949afb6cb0c9d41585909-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2008/FeatureServer', "layer": 0},  # Historic Perimeters 2008
    '86d37ca795894409883bb46b84c2adb6-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Incident_Locations_Last24h/FeatureServer', "layer": 0},  # New Starts - Wildland Fire Incident Locations (Last 24 Hours)
    '894926a4714949259b7e6c230be36372-2': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2025/FeatureServer', "layer": 2},  # Event Point
    '894926a4714949259b7e6c230be36372-4': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2025/FeatureServer', "layer": 4},  # Event Line
    '894926a4714949259b7e6c230be36372-5': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2025/FeatureServer', "layer": 5},  # Perimeter Line
    '894926a4714949259b7e6c230be36372-6': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Operational_Data_Archive_2025/FeatureServer', "layer": 6},  # Event Polygon
    '9cad8f424c3c4e1fb72d458869469caf-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2007/FeatureServer', "layer": 0},  # Historic Perimeters 2007
    '9fd76e1a84934a8997777d7fbd7ed293-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2011/FeatureServer', "layer": 0},  # Historic Perimeters 2011
    'a829aefbe4e5471490d8f3d47ca5410d-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_GeoMAC_Perimeters_2019/FeatureServer', "layer": 0},  # Historic Perimeters 2019
    'b4402f7887ca4ea9a6189443f220ef28-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Incident_Locations/FeatureServer', "layer": 0},  # Wildland Fire Incident Locations
    'b8793ce5b2414754b804daf783fcc34a-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/DMP_National_Dispatch_Locations_Public/FeatureServer', "layer": 0},  # National Dispatch Locations Public
    'b8f4033069f141729ffb298b7418b653-0': {"url": 'https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/MODIS_Thermal_v1/FeatureServer', "layer": 0},  # MODIS Thermal (Last 48 hours)
    'b8f4033069f141729ffb298b7418b653-1': {"url": 'https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/MODIS_Thermal_v1/FeatureServer', "layer": 1},  # MODIS Thermal (Last 7 days)
    'c0175d834e9b43e8aa0f72ca3f4eef68-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2001/FeatureServer', "layer": 0},  # Historic Perimeters 2001
    'c23e282aae534f798e6e231a2cfe584a-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/ProtectingUnits_Public/FeatureServer', "layer": 0},  # Protecting Units Public
    'c30d1f923212468ab6f44bd7d19ca1c1-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/CA_WF_Direct_Protection_Areas_Public/FeatureServer', "layer": 0},  # California Wildland Fire Direct Protection Areas
    'cc50b6ca69734e4180d5399006058e58-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Nat_PODs_Public/FeatureServer', "layer": 0},  # PODs Line
    'cc50b6ca69734e4180d5399006058e58-1': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Nat_PODs_Public/FeatureServer', "layer": 1},  # PODs Poly
    'cc50b6ca69734e4180d5399006058e58-2': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Nat_PODs_Public/FeatureServer', "layer": 2},  # PODs Lines HAVE Poly
    'd1c32af3212341869b3c810f1a215824-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_Current/FeatureServer', "layer": 0},  # WFIGS Current Interagency Fire Perimeters
    'dece90af1a0242dcbf0ca36d30276aa3-0': {"url": 'https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/Satellite_VIIRS_Thermal_Hotspots_and_Fire_Activity/FeatureServer', "layer": 0},  # Satellite (VIIRS) Thermal Hotspots and Fire Activity
    'dffc3c4f66c34ec48dbfa58041600ca5-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2002/FeatureServer', "layer": 0},  # Historic Perimeters 2002
    'e02b85c0ea784ce7bd8add7ae3d293d0-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/InterAgencyFirePerimeterHistory_All_Years_View/FeatureServer', "layer": 0},  # InterAgencyFirePerimeterHistory All Years View
    'e51384680f7e47bf9a93c8b61e83bdfc-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2018/FeatureServer', "layer": 0},  # Historic Perimeters 2018
    'e8c709bf6d3c4e99a64de1360553a07a-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2014/FeatureServer', "layer": 0},  # Historic Perimeters 2014
    'eaa333df1850483abdd0465f86212e03-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/IMSR_Incident_Locations_View_Final_Occurrence_Historical/FeatureServer', "layer": 0},  # IMSR Incident Locations View: Final Occurrence Historical
    'ebcb160b82a242369caf0b7ed9640ac7-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Incident_Feature_Service_2017/FeatureServer', "layer": 0},  # EventPoint2017
    'ebcb160b82a242369caf0b7ed9640ac7-1': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Incident_Feature_Service_2017/FeatureServer', "layer": 1},  # EventLine2017
    'ebcb160b82a242369caf0b7ed9640ac7-2': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Incident_Feature_Service_2017/FeatureServer', "layer": 2},  # EventPolygon2017
    'ebcd309a37844cecb0f68d7c7530ed88-0': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 0},  # Point Actions
    'ebcd309a37844cecb0f68d7c7530ed88-1': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 1},  # Line Actions
    'ebcd309a37844cecb0f68d7c7530ed88-10': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 10},  # Statuses
    'ebcd309a37844cecb0f68d7c7530ed88-11': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 11},  # Funding
    'ebcd309a37844cecb0f68d7c7530ed88-12': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 12},  # DetailedFundingSources
    'ebcd309a37844cecb0f68d7c7530ed88-13': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 13},  # Carryover
    'ebcd309a37844cecb0f68d7c7530ed88-14': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 14},  # CarryoverReasons
    'ebcd309a37844cecb0f68d7c7530ed88-15': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 15},  # CancelReasons
    'ebcd309a37844cecb0f68d7c7530ed88-16': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 16},  # CanceledFeature
    'ebcd309a37844cecb0f68d7c7530ed88-17': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 17},  # CategoryTypes
    'ebcd309a37844cecb0f68d7c7530ed88-18': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 18},  # Measurements
    'ebcd309a37844cecb0f68d7c7530ed88-19': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 19},  # Interagency
    'ebcd309a37844cecb0f68d7c7530ed88-2': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 2},  # Polygon Actions
    'ebcd309a37844cecb0f68d7c7530ed88-3': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 3},  # Projects
    'ebcd309a37844cecb0f68d7c7530ed88-4': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 4},  # Actions
    'ebcd309a37844cecb0f68d7c7530ed88-5': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 5},  # EstimatedActual
    'ebcd309a37844cecb0f68d7c7530ed88-6': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 6},  # TreatmentActivityGroup
    'ebcd309a37844cecb0f68d7c7530ed88-7': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 7},  # TreatmentActivityGroupItems
    'ebcd309a37844cecb0f68d7c7530ed88-8': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 8},  # Units
    'ebcd309a37844cecb0f68d7c7530ed88-9': {"url": 'https://ifprs.firenet.gov/arcgis/rest/services/OpenData/IFPRS_Open_Data/FeatureServer', "layer": 9},  # FundingSources
    'ecb98eb4836e4524a5d27e9c767c8f12-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2005/FeatureServer', "layer": 0},  # Historic Perimeters 2005
    'ee373d927c2547f89330639e2d178d8e-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2013/FeatureServer', "layer": 0},  # Historic Perimeters 2013
    'ef25d7e8c9f3499ba9e3d8e09606e488-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_Combined_2000_2018/FeatureServer', "layer": 0},  # Historic Perimeters Combined 2000-2018 GeoMAC
    'efdb8630cdcb4ecf89968a36efe1473f-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2009/FeatureServer', "layer": 0},  # Historic Perimeters 2009
    'fe3e824f60254901b9408143870769fb-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2012/FeatureServer', "layer": 0},  # Historic Perimeters 2012
    'fe9a015608f04d4aa614548a6afa6dd8-0': {"url": 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_Geomac_Perimeters_2004/FeatureServer', "layer": 0},  # Historic Perimeters 2004
}
