import httpx
from subsets_utils import get

AUTO = "https://data.berkeleyearth.org/auto/Regional/TAVG/Text/{slug}-TAVG-Trend.txt"

CONTINENTS = [
    "africa", "asia", "europe", "north-america", "south-america", "oceania",
    "antarctica", "australia", "northern-hemisphere", "southern-hemisphere",
    "global", "world", "contiguous-united-states",
]

COUNTRIES = [
    "united-states", "united-kingdom", "france", "germany", "china", "india",
    "brazil", "russia", "canada", "australia", "japan", "mexico", "italy",
    "spain", "south-korea", "korea", "north-korea", "indonesia", "saudi-arabia",
    "turkey", "switzerland", "netherlands", "argentina", "sweden", "norway",
    "poland", "belgium", "thailand", "ireland", "austria", "nigeria", "egypt",
    "south-africa", "vietnam", "bangladesh", "iran", "iraq", "pakistan",
    "new-zealand", "greece", "portugal", "denmark", "finland", "czech-republic",
    "czechia", "romania", "ukraine", "hungary", "israel", "chile", "colombia",
    "peru", "venezuela", "kenya", "ethiopia", "morocco", "algeria", "ghana",
    "ivory-coast", "cote-d-ivoire", "philippines", "malaysia", "singapore",
    "myanmar", "burma", "cambodia", "laos", "nepal", "sri-lanka", "afghanistan",
    "kazakhstan", "uzbekistan", "united-arab-emirates", "qatar", "kuwait",
    "iceland", "luxembourg", "croatia", "serbia", "bulgaria", "slovakia",
    "slovenia", "lithuania", "latvia", "estonia", "belarus", "moldova",
    "cuba", "jamaica", "haiti", "dominican-republic", "guatemala", "honduras",
    "nicaragua", "costa-rica", "panama", "ecuador", "bolivia", "paraguay",
    "uruguay",
]

US_STATES = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia-(state)", "georgia", "hawaii",
    "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
    "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new-hampshire", "new-jersey",
    "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
    "south-dakota", "tennessee", "texas", "utah", "vermont", "virginia",
    "washington", "west-virginia", "wisconsin", "wyoming",
]


def check(slugs, label):
    ok, bad = [], []
    for s in slugs:
        url = AUTO.format(slug=s)
        try:
            r = get(url, timeout=(10.0, 60.0))
            if r.status_code == 200 and len(r.text) > 1000:
                ok.append(s)
            else:
                bad.append((s, r.status_code))
        except httpx.HTTPStatusError as e:
            bad.append((s, e.response.status_code))
        except Exception as e:
            bad.append((s, type(e).__name__))
    print(f"\n=== {label}: {len(ok)}/{len(slugs)} ok")
    print("OK :", ok)
    print("BAD:", bad)


check(CONTINENTS, "continents")
check(COUNTRIES, "countries")
check(US_STATES, "us_states")
