# Seed lists for the TwitchTracker connector.
#
# TwitchTracker exposes only per-entity summary endpoints and NO list/catalog
# endpoint, and scraping its ranking pages is prohibited. So the set of channels
# and game categories to query is curated data, not logic — it lives here.
# These are well-known, long-running Twitch channels and the major Twitch game
# categories. Entities the API does not track (returns an empty `{}`) are simply
# skipped at fetch time, so an occasional stale entry here is harmless.

CHANNEL_LOGINS = [
    "xqc", "caseoh_", "jynxzi", "ironmouse", "hasanabi", "pokimane",
    "auronplay", "ibai", "tarik", "summit1g", "timthetatman", "rubius",
    "shroud", "ninja", "tfue", "fextralife", "zackrawrr", "gaules",
    "loud_coringa", "elspreen", "lirik", "sodapoppin", "nickmercs",
    "tommyinnit", "ludwig", "moistcr1tikal", "amouranth", "myth",
    "sykkuno", "valkyrae", "disguisedtoast", "mizkif", "esfandtv",
    "asmongold", "trainwreckstv", "drdisrespect", "clix", "bugha",
    "tenz", "shahzamtv", "alanzoka", "cellbit", "casimito", "felps",
    "ac7ionman", "kyedae", "scump", "knut", "quackity", "roshtein",
]

# Major Twitch game/category names. The /games/summary endpoint accepts the
# full category name (URL-encoded) or the numeric Twitch game id; names are
# more legible and equally stable.
GAMES = [
    "Just Chatting", "League of Legends", "Grand Theft Auto V", "VALORANT",
    "Fortnite", "Counter-Strike", "Dota 2", "Minecraft", "Call of Duty",
    "World of Warcraft", "Apex Legends", "Overwatch 2", "Marvel Rivals",
    "Teamfight Tactics", "EA Sports FC 25", "PUBG: BATTLEGROUNDS",
    "Rust", "Path of Exile 2", "Hearthstone", "Rocket League",
    "Dead by Daylight", "The Finals", "Escape from Tarkov", "Slots",
    "Special Events", "Music", "ELDEN RING", "Baldur's Gate 3",
    "Pokemon", "Sons of the Forest", "Lethal Company", "Palworld",
    "Helldivers 2", "Diablo IV", "Red Dead Redemption 2", "Sea of Thieves",
    "Old School RuneScape", "FIFA", "NBA 2K25", "Black Myth: Wukong",
    "Honkai: Star Rail", "Genshin Impact", "Schedule I",
    "Marvel's Spider-Man 2", "Chess",
]
