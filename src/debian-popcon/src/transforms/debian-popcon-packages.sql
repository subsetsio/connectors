SELECT
    rank,
    name AS package,
    inst,
    vote,
    old,
    recent,
    no_files,
    maintainer
FROM "debian-popcon-packages"
