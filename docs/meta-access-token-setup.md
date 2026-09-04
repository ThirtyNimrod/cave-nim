# Meta access token setup

`META_ACCESS_TOKEN` and `IG_USER_ID` power `src/publisher.py` — the Instagram
Graph API calls that create a media container, poll it, and publish it.
Nothing else in the pipeline touches these credentials.

This is the most involved credential in the project because it depends on
Meta's Business/Developer platform, not just a single API key. The exact menu
names in Meta's developer console shift over time, so treat the steps below
as the current shape of the process and cross-check against Meta's official
docs if something doesn't match what you see:
[developers.facebook.com/docs/instagram-platform/instagram-graph-api/content-publishing](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/content-publishing)

## Prerequisites

1. Your Instagram account must be a **Professional account** (Business or
   Creator) — Instagram app → Settings → Account type.
2. That account must be linked to a **Facebook Page** you control.

## Generate the token

1. Create an app at [developers.facebook.com/apps](https://developers.facebook.com/apps) → **Create App** → choose the **Business** app type.
2. In the app dashboard, add the Instagram Graph API product (this may be listed under Facebook Login for Business, depending on the current console).
3. Open the [Graph API Explorer](https://developers.facebook.com/tools/explorer), select your app, and generate a **User Access Token** with these permissions: `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`.
4. This token is short-lived (about an hour). Exchange it for a **long-lived token** (about 60 days):

   ```
   GET https://graph.facebook.com/v21.0/oauth/access_token
       ?grant_type=fb_exchange_token
       &client_id={your-app-id}
       &client_secret={your-app-secret}
       &fb_exchange_token={short-lived-token}
   ```

5. Find your Facebook Page ID:

   ```
   GET https://graph.facebook.com/v21.0/me/accounts?access_token={long-lived-token}
   ```

6. Find your `IG_USER_ID` (the Instagram-scoped id — not your @handle) from that Page:

   ```
   GET https://graph.facebook.com/v21.0/{page-id}?fields=instagram_business_account&access_token={long-lived-token}
   ```

`META_ACCESS_TOKEN` is the long-lived token from step 4. `IG_USER_ID` is the
id returned in step 6.

**Token expiry**: long-lived tokens last roughly 60 days and do not
auto-renew. Plan to repeat step 4 periodically — `publish.yml` will start
failing with an authentication error once the token expires, with no advance
warning (see [future-enhancements.md](future-enhancements.md) for an idea to
close that gap).

## Where it goes

**Local development** — in `.env`:

```
META_ACCESS_TOKEN=your-long-lived-token
IG_USER_ID=your-numeric-ig-user-id
```

**GitHub Actions** — as two repo secrets (**Settings → Secrets and variables
→ Actions → New repository secret**): `META_ACCESS_TOKEN` and `IG_USER_ID`.

## Test it

**Check the token is valid at all** (independent of this project):

```
GET https://graph.facebook.com/debug_token?input_token={token}&access_token={token}
```

This also shows the token's expiry timestamp and granted scopes.

**Exercise the real pipeline without posting anything**:

```bash
python main.py publish --dry-run
```

This requires at least one entry in `canon.json` whose image is already
pushed to GitHub (`assets/rendered/*.png` on `main`) — the Graph API fetches
the image by public URL (`raw.githubusercontent.com/...`), not by local file
upload, so the repo must be pushed first. `--dry-run` creates and polls the
media container against the real API but stops before the final
`media_publish` call, so nothing goes live.

**Actually publish one post** (only once you're ready):

```bash
python main.py publish
```
