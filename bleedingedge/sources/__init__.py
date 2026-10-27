"""One module per source. Each exposes dates(phrases, start, end) -> list[date]:
the dates of matching items, de-duplicated across phrases, and query_url(...) so
every count in the report can link to the query that produced it."""
