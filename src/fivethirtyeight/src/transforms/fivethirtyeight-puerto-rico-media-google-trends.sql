-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Day" AS day,
    """Hurricane Harvey"": (United States)" AS hurricane_harvey_united_states,
    """Hurricane Irma"": (United States)" AS hurricane_irma_united_states,
    """Hurricane Maria"": (United States)" AS hurricane_maria_united_states,
    """Hurricane Jose"": (United States)" AS hurricane_jose_united_states
FROM "fivethirtyeight-puerto-rico-media-google-trends"
