"""FiveThirtyEight data connector.

Source: the public github.com/fivethirtyeight/data repository (CC BY 4.0 data,
MIT code). Each published subset is one CSV file in the repo, fetched in full
from the raw.githubusercontent.com CDN (the 'raw_files' mechanism). This is a
stateless full re-pull: every refresh re-fetches each CSV and overwrites - the
corpus is ~225MB across 128 files, cheap to pull whole, and the source exposes
no incremental/since filter (full corpus per refresh).

The collect entity id is the repo-relative path minus '.csv' with '/' flattened
to '-' (so the published Delta table name is a flat slug, not a nested R2 path).
That flattening is irreversible, so ENTITY_PATHS maps each spec id back to its
real repo path for fetching.
"""
import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://raw.githubusercontent.com/fivethirtyeight/data/master/"

# spec id -> real repo path. Carried explicitly because the id is a flattened,
# lower-cased slug that cannot be reversed to the real path.
ENTITY_PATHS = {
    'fivethirtyeight-airline-safety-airline-safety': 'airline-safety/airline-safety.csv',
    'fivethirtyeight-alcohol-consumption-drinks': 'alcohol-consumption/drinks.csv',
    'fivethirtyeight-avengers-avengers': 'avengers/avengers.csv',
    'fivethirtyeight-bad-drivers-bad-drivers': 'bad-drivers/bad-drivers.csv',
    'fivethirtyeight-bechdel-movies': 'bechdel/movies.csv',
    'fivethirtyeight-biopics-biopics': 'biopics/biopics.csv',
    'fivethirtyeight-births-us-births-1994-2003-cdc-nchs': 'births/US_births_1994-2003_CDC_NCHS.csv',
    'fivethirtyeight-births-us-births-2000-2014-ssa': 'births/US_births_2000-2014_SSA.csv',
    'fivethirtyeight-bob-ross-elements-by-episode': 'bob-ross/elements-by-episode.csv',
    'fivethirtyeight-cabinet-turnover-cabinet-turnover': 'cabinet-turnover/cabinet-turnover.csv',
    'fivethirtyeight-candy-power-ranking-candy-data': 'candy-power-ranking/candy-data.csv',
    'fivethirtyeight-classic-rock-classic-rock-raw-data': 'classic-rock/classic-rock-raw-data.csv',
    'fivethirtyeight-classic-rock-classic-rock-song-list': 'classic-rock/classic-rock-song-list.csv',
    'fivethirtyeight-college-majors-all-ages': 'college-majors/all-ages.csv',
    'fivethirtyeight-college-majors-grad-students': 'college-majors/grad-students.csv',
    'fivethirtyeight-college-majors-majors-list': 'college-majors/majors-list.csv',
    'fivethirtyeight-college-majors-recent-grads': 'college-majors/recent-grads.csv',
    'fivethirtyeight-college-majors-women-stem': 'college-majors/women-stem.csv',
    'fivethirtyeight-comic-characters-dc-wikia-data': 'comic-characters/dc-wikia-data.csv',
    'fivethirtyeight-comic-characters-marvel-wikia-data': 'comic-characters/marvel-wikia-data.csv',
    'fivethirtyeight-comma-survey-comma-survey': 'comma-survey/comma-survey.csv',
    'fivethirtyeight-congress-age-congress-terms': 'congress-age/congress-terms.csv',
    'fivethirtyeight-congress-demographics-data-aging-congress': 'congress-demographics/data_aging_congress.csv',
    'fivethirtyeight-congress-generic-ballot-generic-topline-historical': 'congress-generic-ballot/generic_topline_historical.csv',
    'fivethirtyeight-congress-resignations-congressional-resignations': 'congress-resignations/congressional_resignations.csv',
    'fivethirtyeight-cousin-marriage-cousin-marriage-data': 'cousin-marriage/cousin-marriage-data.csv',
    'fivethirtyeight-covid-geography-mmsa-icu-beds': 'covid-geography/mmsa-icu-beds.csv',
    'fivethirtyeight-daily-show-guests-daily-show-guests': 'daily-show-guests/daily_show_guests.csv',
    'fivethirtyeight-drug-use-by-age-drug-use-by-age': 'drug-use-by-age/drug-use-by-age.csv',
    'fivethirtyeight-fandango-fandango-score-comparison': 'fandango/fandango_score_comparison.csv',
    'fivethirtyeight-fandango-fandango-scrape': 'fandango/fandango_scrape.csv',
    'fivethirtyeight-flying-etiquette-survey-flying-etiquette': 'flying-etiquette-survey/flying-etiquette.csv',
    'fivethirtyeight-hate-crimes-hate-crimes': 'hate-crimes/hate_crimes.csv',
    'fivethirtyeight-marriage-both-sexes': 'marriage/both_sexes.csv',
    'fivethirtyeight-marriage-divorce': 'marriage/divorce.csv',
    'fivethirtyeight-marriage-men': 'marriage/men.csv',
    'fivethirtyeight-marriage-women': 'marriage/women.csv',
    'fivethirtyeight-masculinity-survey-masculinity-survey': 'masculinity-survey/masculinity-survey.csv',
    'fivethirtyeight-masculinity-survey-raw-responses': 'masculinity-survey/raw-responses.csv',
    'fivethirtyeight-mlb-allstar-teams-allstar-player-talent': 'mlb-allstar-teams/allstar_player_talent.csv',
    'fivethirtyeight-mlb-allstar-teams-allstar-team-talent': 'mlb-allstar-teams/allstar_team_talent.csv',
    'fivethirtyeight-most-common-name-adjusted-name-combinations-list': 'most-common-name/adjusted-name-combinations-list.csv',
    'fivethirtyeight-most-common-name-adjusted-name-combinations-matrix': 'most-common-name/adjusted-name-combinations-matrix.csv',
    'fivethirtyeight-most-common-name-adjustments': 'most-common-name/adjustments.csv',
    'fivethirtyeight-most-common-name-aging-curve': 'most-common-name/aging-curve.csv',
    'fivethirtyeight-most-common-name-independent-name-combinations-by-pop': 'most-common-name/independent-name-combinations-by-pop.csv',
    'fivethirtyeight-most-common-name-new-top-firstnames': 'most-common-name/new-top-firstNames.csv',
    'fivethirtyeight-most-common-name-new-top-surnames': 'most-common-name/new-top-surnames.csv',
    'fivethirtyeight-most-common-name-state-pop': 'most-common-name/state-pop.csv',
    'fivethirtyeight-most-common-name-surnames': 'most-common-name/surnames.csv',
    'fivethirtyeight-murder-2016-murder-2015-final': 'murder_2016/murder_2015_final.csv',
    'fivethirtyeight-murder-2016-murder-2016-prelim': 'murder_2016/murder_2016_prelim.csv',
    'fivethirtyeight-nba-elo-nbaallelo': 'nba-elo/nbaallelo.csv',
    'fivethirtyeight-nba-raptor-historical-raptor-by-player': 'nba-raptor/historical_RAPTOR_by_player.csv',
    'fivethirtyeight-nba-raptor-historical-raptor-by-team': 'nba-raptor/historical_RAPTOR_by_team.csv',
    'fivethirtyeight-nba-raptor-modern-raptor-by-player': 'nba-raptor/modern_RAPTOR_by_player.csv',
    'fivethirtyeight-nba-raptor-modern-raptor-by-team': 'nba-raptor/modern_RAPTOR_by_team.csv',
    'fivethirtyeight-next-bechdel-nextbechdel-alltests': 'next-bechdel/nextBechdel_allTests.csv',
    'fivethirtyeight-next-bechdel-nextbechdel-castgender': 'next-bechdel/nextBechdel_castGender.csv',
    'fivethirtyeight-next-bechdel-nextbechdel-crewgender': 'next-bechdel/nextBechdel_crewGender.csv',
    'fivethirtyeight-non-voters-nonvoters-data': 'non-voters/nonvoters_data.csv',
    'fivethirtyeight-nutrition-studies-p-values-analysis': 'nutrition-studies/p_values_analysis.csv',
    'fivethirtyeight-nutrition-studies-raw-anonymized-data': 'nutrition-studies/raw_anonymized_data.csv',
    'fivethirtyeight-partisan-lean-2018-fivethirtyeight-partisan-lean-districts': 'partisan-lean/2018/fivethirtyeight_partisan_lean_DISTRICTS.csv',
    'fivethirtyeight-partisan-lean-2018-fivethirtyeight-partisan-lean-states': 'partisan-lean/2018/fivethirtyeight_partisan_lean_STATES.csv',
    'fivethirtyeight-partisan-lean-2020-fivethirtyeight-partisan-lean-districts': 'partisan-lean/2020/fivethirtyeight_partisan_lean_DISTRICTS.csv',
    'fivethirtyeight-partisan-lean-2020-fivethirtyeight-partisan-lean-states': 'partisan-lean/2020/fivethirtyeight_partisan_lean_STATES.csv',
    'fivethirtyeight-partisan-lean-2021-fivethirtyeight-partisan-lean-districts': 'partisan-lean/2021/fivethirtyeight_partisan_lean_DISTRICTS.csv',
    'fivethirtyeight-partisan-lean-2021-fivethirtyeight-partisan-lean-states': 'partisan-lean/2021/fivethirtyeight_partisan_lean_STATES.csv',
    'fivethirtyeight-partisan-lean-fivethirtyeight-partisan-lean-districts': 'partisan-lean/fivethirtyeight_partisan_lean_DISTRICTS.csv',
    'fivethirtyeight-partisan-lean-fivethirtyeight-partisan-lean-states': 'partisan-lean/fivethirtyeight_partisan_lean_STATES.csv',
    'fivethirtyeight-pew-religions-current': 'pew-religions/current.csv',
    'fivethirtyeight-police-deaths-all-data': 'police-deaths/all_data.csv',
    'fivethirtyeight-police-deaths-clean-data': 'police-deaths/clean_data.csv',
    'fivethirtyeight-police-killings-police-killings': 'police-killings/police_killings.csv',
    'fivethirtyeight-police-locals-police-locals': 'police-locals/police-locals.csv',
    'fivethirtyeight-political-elasticity-scores-elasticity-by-district': 'political-elasticity-scores/elasticity-by-district.csv',
    'fivethirtyeight-political-elasticity-scores-elasticity-by-state': 'political-elasticity-scores/elasticity-by-state.csv',
    'fivethirtyeight-polls-2024-averages-presidential-general-averages-2024-09-12-uncorrected': 'polls/2024-averages/presidential_general_averages_2024-09-12_uncorrected.csv',
    'fivethirtyeight-polls-2024-averages-presidential-primary-averages-2024': 'polls/2024-averages/presidential_primary_averages_2024.csv',
    'fivethirtyeight-polls-old-model-2024-presidential-primary-averages-old-model': 'polls/old_model/2024_presidential_primary_averages_old_model.csv',
    'fivethirtyeight-polls-old-model-donald-trump-favorability-old-model': 'polls/old_model/donald_trump_favorability_old_model.csv',
    'fivethirtyeight-polls-old-model-generic-ballot-averages-old-model': 'polls/old_model/generic_ballot_averages_old_model.csv',
    'fivethirtyeight-polls-old-model-joe-biden-approval-old-model': 'polls/old_model/joe_biden_approval_old_model.csv',
    'fivethirtyeight-polls-old-model-kamala-harris-approval-old-model': 'polls/old_model/kamala_harris_approval_old_model.csv',
    'fivethirtyeight-polls-old-model-mike-pence-favorability-old-model': 'polls/old_model/mike_pence_favorability_old_model.csv',
    'fivethirtyeight-polls-old-model-nikki-haley-favorability-old-model': 'polls/old_model/nikki_haley_favorability_old_model.csv',
    'fivethirtyeight-polls-old-model-ron-desantis-favorability-old-model': 'polls/old_model/ron_desantis_favorability_old_model.csv',
    'fivethirtyeight-polls-pres-pollaverages-1968-2016': 'polls/pres_pollaverages_1968-2016.csv',
    'fivethirtyeight-polls-pres-primary-avgs-1980-2016': 'polls/pres_primary_avgs_1980-2016.csv',
    'fivethirtyeight-pollster-ratings-2016-pollster-ratings': 'pollster-ratings/2016/pollster-ratings.csv',
    'fivethirtyeight-pollster-ratings-2016-raw-polls': 'pollster-ratings/2016/raw-polls.csv',
    'fivethirtyeight-pollster-ratings-2018-pollster-ratings': 'pollster-ratings/2018/pollster-ratings.csv',
    'fivethirtyeight-pollster-ratings-2018-raw-polls': 'pollster-ratings/2018/raw-polls.csv',
    'fivethirtyeight-pollster-ratings-2019-pollster-ratings': 'pollster-ratings/2019/pollster-ratings.csv',
    'fivethirtyeight-pollster-ratings-2019-raw-polls': 'pollster-ratings/2019/raw-polls.csv',
    'fivethirtyeight-pollster-ratings-2020-pollster-ratings': 'pollster-ratings/2020/pollster-ratings.csv',
    'fivethirtyeight-pollster-ratings-2020-raw-polls': 'pollster-ratings/2020/raw-polls.csv',
    'fivethirtyeight-pollster-ratings-2021-pollster-ratings': 'pollster-ratings/2021/pollster-ratings.csv',
    'fivethirtyeight-pollster-ratings-2021-raw-polls': 'pollster-ratings/2021/raw-polls.csv',
    'fivethirtyeight-pollster-ratings-2023-pollster-ratings': 'pollster-ratings/2023/pollster-ratings.csv',
    'fivethirtyeight-pollster-ratings-2023-raw-polls': 'pollster-ratings/2023/raw-polls.csv',
    'fivethirtyeight-pollster-ratings-pollster-ratings-combined': 'pollster-ratings/pollster-ratings-combined.csv',
    'fivethirtyeight-pollster-ratings-raw-polls': 'pollster-ratings/raw_polls.csv',
    'fivethirtyeight-redlining-metro-grades': 'redlining/metro-grades.csv',
    'fivethirtyeight-redlining-zone-block-matches': 'redlining/zone-block-matches.csv',
    'fivethirtyeight-religion-survey-religion-survey-results': 'religion-survey/religion-survey-results.csv',
    'fivethirtyeight-star-wars-survey-starwars': 'star-wars-survey/StarWars.csv',
    'fivethirtyeight-steak-survey-steak-risk-survey': 'steak-survey/steak-risk-survey.csv',
    'fivethirtyeight-tarantino-tarantino': 'tarantino/tarantino.csv',
    'fivethirtyeight-terrorism-country-stats-1993-appendix2': 'terrorism/country_stats_1993_appendix2.csv',
    'fivethirtyeight-terrorism-eu-terrorism-fatalities-by-country': 'terrorism/eu_terrorism_fatalities_by_country.csv',
    'fivethirtyeight-terrorism-eu-terrorism-fatalities-by-year': 'terrorism/eu_terrorism_fatalities_by_year.csv',
    'fivethirtyeight-terrorism-france-terrorism-fatalities-by-year': 'terrorism/france_terrorism_fatalities_by_year.csv',
    'fivethirtyeight-unisex-names-aging-curve': 'unisex-names/aging_curve.csv',
    'fivethirtyeight-unisex-names-unisex-names-table': 'unisex-names/unisex_names_table.csv',
    'fivethirtyeight-urbanization-index-urbanization-census-tract': 'urbanization-index/urbanization-census-tract.csv',
    'fivethirtyeight-urbanization-index-urbanization-state': 'urbanization-index/urbanization-state.csv',
    'fivethirtyeight-us-weather-history-kclt': 'us-weather-history/KCLT.csv',
    'fivethirtyeight-us-weather-history-kcqt': 'us-weather-history/KCQT.csv',
    'fivethirtyeight-us-weather-history-khou': 'us-weather-history/KHOU.csv',
    'fivethirtyeight-us-weather-history-kind': 'us-weather-history/KIND.csv',
    'fivethirtyeight-us-weather-history-kjax': 'us-weather-history/KJAX.csv',
    'fivethirtyeight-us-weather-history-kmdw': 'us-weather-history/KMDW.csv',
    'fivethirtyeight-us-weather-history-knyc': 'us-weather-history/KNYC.csv',
    'fivethirtyeight-us-weather-history-kphl': 'us-weather-history/KPHL.csv',
    'fivethirtyeight-us-weather-history-kphx': 'us-weather-history/KPHX.csv',
    'fivethirtyeight-us-weather-history-ksea': 'us-weather-history/KSEA.csv',
}


@transient_retry()
def _fetch(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _to_utf8(content: bytes) -> bytes:
    """Normalize raw bytes to valid UTF-8. Most files are already UTF-8; some
    legacy FiveThirtyEight CSVs (star-wars-survey, biopics, next-bechdel) are
    Windows-1252 and a few carry bytes even cp1252 leaves undefined (0x81,
    0x8f). Decoding cp1252 with errors='replace' renders the common smart-quote
    punctuation correctly and turns the rare undefined byte into U+FFFD instead
    of crashing - and guarantees the parser and downstream DuckDB only ever see
    valid UTF-8."""
    try:
        content.decode("utf-8")
        return content
    except UnicodeDecodeError:
        return content.decode("cp1252", errors="replace").encode("utf-8")


def _parse_csv(content: bytes) -> pa.Table:
    """Parse one CSV to a typed Arrow table. pyarrow infers column types; on any
    conversion failure (ragged/mixed columns) fall back to reading every column
    as a string so the file still publishes. Read as a single block so type
    inference is consistent across the whole file (largest in scope ~50MB)."""
    content = _to_utf8(content)
    read_opts = pacsv.ReadOptions(block_size=512 * 1024 * 1024)
    try:
        return pacsv.read_csv(io.BytesIO(content), read_options=read_opts)
    except (pa.ArrowInvalid, pa.ArrowNotImplementedError):
        import pandas as pd
        df = pd.read_csv(io.BytesIO(content), dtype=str, low_memory=False)
        return pa.Table.from_pandas(df, preserve_index=False)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    url = BASE + ENTITY_PATHS[node_id]
    table = _parse_csv(_fetch(url))
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in ENTITY_PATHS
]

# Per-file published grain (key) and primary observation-period column
# (temporal). Purely declarative, keyed by download spec id. Only files with a
# confidently-natural grain / period are listed; heterogeneous survey-response,
# event-log, and pivot/matrix files (no confirmed unique identifier) are left
# undeclared. Keys are drawn from profiler-confirmed unique columns; temporals
# from profiler date-typed columns. Entries default to (None, None) = undeclared.
GRAIN: dict[str, tuple[tuple[str, ...] | None, str | None]] = {
    "fivethirtyeight-airline-safety-airline-safety": (("airline",), None),
    "fivethirtyeight-alcohol-consumption-drinks": (("country",), None),
    "fivethirtyeight-avengers-avengers": (("URL",), None),
    "fivethirtyeight-bad-drivers-bad-drivers": (("State",), None),
    "fivethirtyeight-bechdel-movies": (("imdb",), None),
    "fivethirtyeight-bob-ross-elements-by-episode": (("EPISODE",), None),
    "fivethirtyeight-candy-power-ranking-candy-data": (("competitorname",), None),
    "fivethirtyeight-classic-rock-classic-rock-raw-data": (("UNIQUE_ID",), None),
    "fivethirtyeight-classic-rock-classic-rock-song-list": (("COMBINED",), "Release Year"),
    "fivethirtyeight-college-majors-all-ages": (("Major_code",), None),
    "fivethirtyeight-college-majors-grad-students": (("Major_code",), None),
    "fivethirtyeight-college-majors-majors-list": (("FOD1P",), None),
    "fivethirtyeight-college-majors-recent-grads": (("Major_code",), None),
    "fivethirtyeight-college-majors-women-stem": (("Major_code",), None),
    "fivethirtyeight-comic-characters-dc-wikia-data": (("page_id",), None),
    "fivethirtyeight-comic-characters-marvel-wikia-data": (("page_id",), None),
    "fivethirtyeight-comma-survey-comma-survey": (("RespondentID",), None),
    "fivethirtyeight-congress-generic-ballot-generic-topline-historical": (("modeldate",), None),
    "fivethirtyeight-cousin-marriage-cousin-marriage-data": (("Country",), None),
    "fivethirtyeight-covid-geography-mmsa-icu-beds": (("MMSA",), None),
    "fivethirtyeight-drug-use-by-age-drug-use-by-age": (("age",), None),
    "fivethirtyeight-fandango-fandango-score-comparison": (("FILM",), None),
    "fivethirtyeight-flying-etiquette-survey-flying-etiquette": (("RespondentID",), None),
    "fivethirtyeight-hate-crimes-hate-crimes": (("state",), None),
    "fivethirtyeight-marriage-both-sexes": (("year",), "date"),
    "fivethirtyeight-marriage-divorce": (("year",), "date"),
    "fivethirtyeight-marriage-men": (("year",), "date"),
    "fivethirtyeight-marriage-women": (("year",), "date"),
    "fivethirtyeight-most-common-name-new-top-firstnames": (("name",), None),
    "fivethirtyeight-most-common-name-new-top-surnames": (("name",), None),
    "fivethirtyeight-most-common-name-state-pop": (("state",), None),
    "fivethirtyeight-most-common-name-surnames": (("name",), None),
    "fivethirtyeight-murder-2016-murder-2015-final": (("city",), None),
    "fivethirtyeight-murder-2016-murder-2016-prelim": (("city",), None),
    "fivethirtyeight-next-bechdel-nextbechdel-alltests": (("movie",), None),
    "fivethirtyeight-non-voters-nonvoters-data": (("RespId",), None),
    "fivethirtyeight-nutrition-studies-raw-anonymized-data": (("ID",), None),
    "fivethirtyeight-partisan-lean-2018-fivethirtyeight-partisan-lean-districts": (("district",), None),
    "fivethirtyeight-partisan-lean-2018-fivethirtyeight-partisan-lean-states": (("state",), None),
    "fivethirtyeight-partisan-lean-2020-fivethirtyeight-partisan-lean-districts": (("district",), None),
    "fivethirtyeight-partisan-lean-2020-fivethirtyeight-partisan-lean-states": (("state",), None),
    "fivethirtyeight-partisan-lean-2021-fivethirtyeight-partisan-lean-districts": (("district",), None),
    "fivethirtyeight-partisan-lean-2021-fivethirtyeight-partisan-lean-states": (("state",), None),
    "fivethirtyeight-partisan-lean-fivethirtyeight-partisan-lean-districts": (("district",), None),
    "fivethirtyeight-partisan-lean-fivethirtyeight-partisan-lean-states": (("state",), None),
    "fivethirtyeight-police-locals-police-locals": (("city",), None),
    "fivethirtyeight-political-elasticity-scores-elasticity-by-district": (("district",), None),
    "fivethirtyeight-political-elasticity-scores-elasticity-by-state": (("state",), None),
    "fivethirtyeight-pollster-ratings-2016-pollster-ratings": (("ID",), None),
    "fivethirtyeight-pollster-ratings-2016-raw-polls": (("pollno",), None),
    "fivethirtyeight-pollster-ratings-2018-pollster-ratings": (("Pollster",), None),
    "fivethirtyeight-pollster-ratings-2018-raw-polls": (("pollno",), None),
    "fivethirtyeight-pollster-ratings-2019-pollster-ratings": (("Pollster Rating ID",), None),
    "fivethirtyeight-pollster-ratings-2019-raw-polls": (("pollno",), None),
    "fivethirtyeight-pollster-ratings-2020-pollster-ratings": (("Pollster Rating ID",), None),
    "fivethirtyeight-pollster-ratings-2020-raw-polls": (("question_id",), None),
    "fivethirtyeight-pollster-ratings-2021-pollster-ratings": (("Pollster Rating ID",), None),
    "fivethirtyeight-pollster-ratings-2021-raw-polls": (("question_id",), None),
    "fivethirtyeight-pollster-ratings-2023-pollster-ratings": (("Pollster Rating ID",), None),
    "fivethirtyeight-pollster-ratings-2023-raw-polls": (("question_id",), None),
    "fivethirtyeight-pollster-ratings-pollster-ratings-combined": (("pollster_rating_id",), None),
    "fivethirtyeight-pollster-ratings-raw-polls": (("question_id",), "polldate"),
    "fivethirtyeight-terrorism-eu-terrorism-fatalities-by-country": (("iyear",), None),
    "fivethirtyeight-terrorism-eu-terrorism-fatalities-by-year": (("iyear",), None),
    "fivethirtyeight-terrorism-france-terrorism-fatalities-by-year": (("iyear",), None),
    "fivethirtyeight-unisex-names-unisex-names-table": (("name",), None),
    "fivethirtyeight-urbanization-index-urbanization-census-tract": (("gisjoin",), None),
    "fivethirtyeight-urbanization-index-urbanization-state": (("state",), None),
    # temporal-only: append/observation logs and poll averages with no single key
    "fivethirtyeight-congress-age-congress-terms": (None, "termstart"),
    "fivethirtyeight-congress-demographics-data-aging-congress": (None, "start_date"),
    "fivethirtyeight-police-deaths-clean-data": (None, "date"),
    "fivethirtyeight-polls-2024-averages-presidential-general-averages-2024-09-12-uncorrected": (None, "date"),
    "fivethirtyeight-polls-2024-averages-presidential-primary-averages-2024": (None, "date"),
    "fivethirtyeight-polls-old-model-2024-presidential-primary-averages-old-model": (None, "date"),
    "fivethirtyeight-polls-old-model-donald-trump-favorability-old-model": (None, "date"),
    "fivethirtyeight-polls-old-model-generic-ballot-averages-old-model": (None, "date"),
    "fivethirtyeight-polls-old-model-joe-biden-approval-old-model": (None, "date"),
    "fivethirtyeight-polls-old-model-kamala-harris-approval-old-model": (None, "date"),
    "fivethirtyeight-polls-old-model-mike-pence-favorability-old-model": (None, "date"),
    "fivethirtyeight-polls-old-model-nikki-haley-favorability-old-model": (None, "date"),
    "fivethirtyeight-polls-old-model-ron-desantis-favorability-old-model": (None, "date"),
    "fivethirtyeight-polls-pres-primary-avgs-1980-2016": (None, "modeldate"),
    "fivethirtyeight-us-weather-history-kclt": (("date",), "date"),
    "fivethirtyeight-us-weather-history-kcqt": (("date",), "date"),
    "fivethirtyeight-us-weather-history-khou": (("date",), "date"),
    "fivethirtyeight-us-weather-history-kind": (("date",), "date"),
    "fivethirtyeight-us-weather-history-kjax": (("date",), "date"),
    "fivethirtyeight-us-weather-history-kmdw": (("date",), "date"),
    "fivethirtyeight-us-weather-history-knyc": (("date",), "date"),
    "fivethirtyeight-us-weather-history-kphl": (("date",), "date"),
    "fivethirtyeight-us-weather-history-kphx": (("date",), "date"),
    "fivethirtyeight-us-weather-history-ksea": (("date",), "date"),
}

# Thin publish pass: each CSV's parsed Arrow table is published as-is (one Delta
# table per file). DuckDB reads the parquet view named after the download id.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        key=GRAIN.get(s.id, (None, None))[0],
        temporal=GRAIN.get(s.id, (None, None))[1],
    )
    for s in DOWNLOAD_SPECS
]
