import sentry_sdk

sentry_sdk.init(
    dsn="https://e0d4fb09adf702b25cdb2da39cf36476@o4507448396218368.ingest.de.sentry.io/4507855997960272",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
