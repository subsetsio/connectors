-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are raw Commons division API items with nested JSON in `record`; use source documentation for the fields inside each item.
SELECT
    "source_entity",
    "source_endpoint",
    "source_skip",
    CAST("record" AS STRUCT(
        DivisionId BIGINT,
        Date TIMESTAMP,
        PublicationUpdated TIMESTAMP,
        Number BIGINT,
        IsDeferred BOOLEAN,
        EVELType VARCHAR,
        EVELCountry VARCHAR,
        Title VARCHAR,
        AyeCount BIGINT,
        NoCount BIGINT,
        DoubleMajorityAyeCount JSON,
        DoubleMajorityNoCount JSON,
        AyeTellers STRUCT(
            MemberId BIGINT,
            "Name" VARCHAR,
            Party VARCHAR,
            SubParty VARCHAR,
            PartyColour VARCHAR,
            PartyAbbreviation VARCHAR,
            MemberFrom VARCHAR,
            ListAs VARCHAR,
            ProxyName JSON
        )[],
        NoTellers STRUCT(
            MemberId BIGINT,
            "Name" VARCHAR,
            Party VARCHAR,
            SubParty VARCHAR,
            PartyColour VARCHAR,
            PartyAbbreviation VARCHAR,
            MemberFrom VARCHAR,
            ListAs VARCHAR,
            ProxyName JSON
        )[],
        Ayes JSON[],
        Noes JSON[],
        FriendlyDescription JSON,
        FriendlyTitle JSON,
        NoVoteRecorded JSON[],
        RemoteVotingStart JSON,
        RemoteVotingEnd JSON
    )) AS "record"
FROM "uk-parliament-commons-votes"
