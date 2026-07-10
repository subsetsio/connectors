# Per-entity fetch configuration for the Global.health connector.
#
# Two fetch surfaces (both CSV, per research):
#   - "github":  a CSV committed to a globaldothealth GitHub repo, fetched from
#                raw.githubusercontent.com pinned to the repo's default branch.
#                (The blob SHAs recorded by collect are GitHub *blob* shas, not
#                commit-ishes, so raw.githubusercontent.com 404s on them — we
#                use the branch ref instead.)
#   - "gateway": an actively-curated outbreak whose latest line list is served
#                from the repo's AWS API-Gateway domain (/web/url?file_name=
#                latest.csv), not committed to git.
#
# Keys are the accept-stage entity ids (the entity union). DOWNLOAD_SPECS in the
# node module derives one spec per key.
ENTITY_CONFIG = {
    # --- actively-curated outbreaks: gateway latest.csv (line lists) ---
    "ebola-uganda-2022": {"mode": "gateway", "domain": "3mmuwilir3"},
    "marburg-equatorial-guinea-2023": {"mode": "gateway", "domain": "l66noa47nk"},
    "mpox-global-2022": {"mode": "gateway", "domain": "7rydd2v2ra"},
    # --- committed CSVs: raw.githubusercontent.com on the default branch ---
    "h1n1-healthmap-2009-2012": {
        "mode": "github", "repo": "h1n1", "ref": "master",
        "path": "HealthMap_H1N1_Global_All_Languages_2009-2012.csv",
        "headerless": True,  # HealthMap dump has no header row
    },
    "omicron-austria": {
        "mode": "github", "repo": "covid19-omicron", "ref": "main",
        "path": "austria/austria.csv",
    },
    "omicron-denmark": {
        "mode": "github", "repo": "covid19-omicron", "ref": "main",
        "path": "denmark/denmark.csv",
    },
    "omicron-europe": {
        "mode": "github", "repo": "covid19-omicron", "ref": "main",
        "path": "europe/europe.csv",
    },
    "omicron-uk-ltla": {
        "mode": "github", "repo": "covid19-omicron", "ref": "main",
        "path": "uk-ltla/uk-ltla.csv",
    },
    "omicron-usa": {
        "mode": "github", "repo": "covid19-omicron", "ref": "main",
        "path": "usa/usa.csv",
    },
    "woah-flu-a-event-4451": {
        "mode": "github", "repo": "woah_wahis_flu_a", "ref": "main",
        "path": "data/Event 4451/1719592393.41658_EVENTID_4451_Epilist.csv",
    },
}
