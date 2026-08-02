# Mission GroundWork Social Scheduler

Mass-schedules LinkedIn, Instagram, Facebook, or Buffer posts from `content/social-queue.json`. GitHub Actions checks the queue every 15 minutes, publishes due records, retries transient failures, and records receipts in `content/social-state.json` so posts are not duplicated.

## Queue fields

Required: `platform`, `scheduled_at`, `text`. Instagram also requires a public `media_url`. Optional: `id`, `title`, `visibility`, `profile_id`.

Use ISO-8601 timestamps with an offset, for example `2026-08-03T13:00:00-04:00`.

## Bulk CSV import

Create `content/social-queue.csv` with headers:

```csv
id,platform,scheduled_at,text,media_url
```

Then run:

```bash
cd tools/social-scheduler
node import-csv.mjs ../../content/social-queue.csv ../../content/social-queue.json
node scheduler.mjs --queue ../../content/social-queue.json --state ../../content/social-state.json --dry-run
```

## GitHub repository secrets

Direct LinkedIn:
- `LINKEDIN_ACCESS_TOKEN`
- `LINKEDIN_AUTHOR_URN`

Meta / Instagram:
- `META_PAGE_ACCESS_TOKEN`
- `META_PAGE_ID`
- `INSTAGRAM_BUSINESS_ID`

Optional Buffer route:
- `BUFFER_ACCESS_TOKEN`
- `BUFFER_PROFILE_ID`

## Safety and operations

- Manual workflow runs default to dry-run.
- Scheduled runs publish only records whose `scheduled_at` is due.
- Stable IDs and the state ledger prevent duplicate publishing.
- HTTP 429 and server failures receive exponential retries.
- Maximum posts per run defaults to 10 and can be changed with `MAX_POSTS_PER_RUN`.
- Never place access tokens in queue files or commits.
