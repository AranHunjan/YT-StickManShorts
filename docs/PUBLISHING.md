# Publishing to YouTube, Instagram, Facebook and TikTok

All four accounts use the same handle: **@KipNDex**.

## Short answer

There's no free tool that posts one upload to all four platforms with no limits. The free setup that works today takes **four uploads per video, about 6 minutes in total**, and you can batch a whole week in one sitting:

| Step | Tool (free) | Posts to |
|---|---|---|
| 1 | **YouTube Studio** (desktop): upload, then *Schedule* | YouTube Shorts |
| 2 | **Meta Business Suite** (business.facebook.com): *Create reel* for the Page, then *Schedule* | Facebook Reels |
| 3 | **Instagram app** (Creator account): new Reel, then *Advanced settings* > *Schedule* | Instagram Reels |
| 4 | **TikTok Studio** (tiktok.com on desktop): upload, then *Schedule* | TikTok |

Instagram and the Facebook Page aren't linked: Meta refused the link on our account (2026-11-06). Linked, Meta Business Suite would post one Reel to both in a single upload. To retry later, open Account Status in Instagram's and Facebook's settings: it shows any restriction and how to ask for a review. New accounts are often restricted for a while.

To get `final.mp4` and `cover.jpg` onto the phone, save them to Google Drive or OneDrive on the PC and open them in the app.

## Why not a single tool (yet)

| Option | Free limit | Verdict |
|---|---|---|
| **Buffer** free plan | 3 channels, 10 queued posts each | Covers 3 of our 4 platforms. You could use it for YouTube, TikTok and Instagram, with Meta Business Suite for Facebook. Fine, but not simpler. |
| **Metricool** free plan | 1 brand, about 20 posts per month | Not enough for 4 platforms × 30 days |
| **Postiz** (open source, self-hosted on your PC) | Unlimited | Real one-click posting to all four, but you need your own developer apps per platform. Until TikTok audits the app, its posts are forced to **private**. A good "phase 2". |
| **Our own publisher** (YouTube Data API, Meta Graph API, TikTok Content Posting API) | Free | Same TikTok audit rule: unaudited apps can only post privately, and to at most 5 users a day. Plan: automate YouTube and Meta first, apply for the TikTok audit, keep TikTok manual until approved. |

Plan: **native tools now** (free, reliable, no approvals). Once the daily pipeline is stable, add automated posting to YouTube and Meta, and apply for the TikTok audit.

## Rules that protect reach

1. **Upload the clean master file everywhere** (`final.mp4` from the pipeline). Never download a TikTok and re-upload it to Reels or Shorts: other platforms' watermarks get downranked. Our own Kip N Dex watermark is fine.
2. **Same video, platform-specific text.** Titles and captions differ a little per platform (see each episode's `upload.md`).
3. **Post at the same time every day.** Pick one slot and keep it; adjust later from analytics.
4. **Made for kids: No** on YouTube (general audience). Category: Education.
5. **Sources go in the description** on YouTube and Facebook, and in the first comment on Instagram and TikTok (their captions are short).
6. **AI labels** ([AI_LABELS.md](AI_LABELS.md), checked 2026-11-06):
   - YouTube: "Altered or synthetic content": **No**. YouTube exempts clearly animated content.
   - Instagram and Facebook: AI label **on**. Meta asks for it on realistic-sounding AI audio, and our voices are AI.
   - TikTok: "AI-generated content": **on**. TikTok asks for it on realistic AI audio, and says the label doesn't affect distribution.
7. **TikTok Creator Rewards** pays only for videos over 1 minute, and TikTok's Creator Academy lists it as open in the US, UK, Germany, Japan, South Korea, France, Mexico and Brazil. Check Creator tools in the TikTok app for your country. Our length cap is in `channel.json`; see [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) before making longer cuts.

## Weekly batch routine (Sunday, about 30 minutes)

1. Review the week's 7 renders.
2. YouTube Studio: upload 7 and schedule each day's slot.
3. Meta Business Suite: create 7 Facebook Reels on the same schedule.
4. Instagram app: upload 7 Reels and schedule each one in the same slot.
5. TikTok Studio: upload and schedule as far ahead as it allows. Post the rest mid-week.
