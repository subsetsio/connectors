-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school",
    "conference",
    "song_name",
    "writers",
    "year",
    "student_writer",
    "official_song",
    "contest",
    "bpm",
    "sec_duration",
    "fight",
    "number_fights",
    "victory",
    "win_won",
    "victory_win_won",
    "rah",
    "nonsense",
    "colors",
    "men",
    "opponents",
    "spelling",
    "trope_count",
    "spotify_id"
FROM "fivethirtyeight-fight-songs-fight-songs"
