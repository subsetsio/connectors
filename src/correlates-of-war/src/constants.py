"""Correlates of War — download map (the entity union, as data not logic).

One entry per rank-accepted collect entity. Each maps the entity id to the
upstream archive file (under https://correlatesofwar.org/wp-content/uploads/)
and the CSV member to extract:

  member = None                 -> the URL is a bare .csv; use the body directly
  member = "dir/file.csv"       -> a member inside the downloaded .zip
  member = "inner.zip!!x.csv"   -> a .csv inside a .zip nested inside the .zip

Verified by download + inspection on 2026-06-21 (latest versions live then).
"""

BASE = "https://correlatesofwar.org/wp-content/uploads/"

# entity_id -> (archive_filename, member_path_or_None)
DOWNLOADS = {
    "arms-technology":            ("ArmsTechnologyV1_2.zip", "ArmsTechnologyV1/cow_arms_tech_long.csv"),
    "trade-dyadic":               ("COW_Trade_4.0.zip", "COW_Trade_4.0/Dyadic_COW_4.0.csv"),
    "trade-national":             ("COW_Trade_4.0.zip", "COW_Trade_4.0/National_COW_4.0.csv"),
    "colonial-contiguity":        ("ColonialContiguity310.zip", "ColonialContiguity310/contcol.csv"),
    "country-codes":              ("COW-country-codes.csv", None),
    "inter-state-war":            ("Inter-StateWarData_v4.0.csv", None),
    "intra-state-war":            ("Intra-State-Wars-v5.1.zip", "INTRA-STATE WARS v5.1 CSV.csv"),
    "extra-state-war":            ("Extra-StateWarData_v4.0.csv", None),
    "non-state-war":              ("Non-StateWarData_v4.0.csv", None),
    "dyadic-interstate-war":      ("Dyadic-Interstate-War-Dataset.zip", "directed_dyadic_war.csv"),
    "dca-agreements":             ("kinne_dca.zip", "kinne_dca/DCAD-v1.0-main.csv"),
    "dca-dyadic":                 ("kinne_dca.zip", "kinne_dca/DCAD-v1.0-dyadic.csv"),
    "diplomatic-exchange":        ("Diplomatic_Exchange_2006.1.zip", "Diplomatic_Exchange_2006v1.csv"),
    "direct-contiguity":          ("DirectContiguity320.zip", "DirectContiguity320/contdir.csv"),
    "alliances-member":           ("version4.1_csv.zip", "version4.1_csv/alliance_v4.1_by_member.csv"),
    "alliances-dyadic":           ("version4.1_csv.zip", "version4.1_csv/alliance_v4.1_by_dyad.csv"),
    "igo-state-year":             ("IGO_stateunit_v2.3.zip", "IGO_stateunit_v2.3.csv"),
    "igo-dyad-year":              ("IGO_dyadunit_v2.3.zip", "IGO_dyadunit_v2.3.csv"),
    "igo-unit":                   ("IGO_igounit_v2.3.zip", "igounit_v2.3.csv"),
    "midloc-dispute":             ("MIDLOC_2.1.zip", "MIDLOCA_2.1.csv"),
    "midloc-incident":            ("MIDLOC_2.1.zip", "MIDLOCI_2.1.csv"),
    "mid-dispute":                ("MID-5-Data-and-Supporting-Materials.zip", "MIDA 5.0.csv"),
    "mid-participant":            ("MID-5-Data-and-Supporting-Materials.zip", "MIDB 5.0.csv"),
    "mid-incident":               ("Incident_Level_5.01.zip", "MIDI_5.01.csv"),
    "mid-incident-participant":   ("Incident_Level_5.01.zip", "MIDIP_5.01.csv"),
    "nmc":                        ("NMCv7.zip", "NMCv7/NMC-v7-abridged.zip!!NMC-70-abridged.csv"),
    "states":                     ("States2024.zip", "States2024/statelist2024.csv"),
    "system-membership":          ("System2024.zip", "System2024/system2024.csv"),
    "major-powers":               ("MajorPowers2024.zip", "MajorPowers2024/majors2024.csv"),
    "territorial-change":         ("terr-changes-v6.zip", "tc2018.csv"),
    "world-religion-national":    ("WRP_national.csv", None),
    "world-religion-regional":    ("WRP_regional.csv", None),
    "world-religion-global":      ("WRP_global.csv", None),
}

ENTITY_IDS = list(DOWNLOADS)
