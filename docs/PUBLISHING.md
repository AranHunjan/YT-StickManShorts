# Publishing to YouTube, Instagram, Facebook and TikTok

All four accounts use the same handle: **@KipNDex**.

## Short answer

There's no free tool that posts one upload to all four platforms with no limits. The free setup that works today takes **three uploads per video, about 5 minutes in total**, and you can batch a whole week in one sitting:

| Step | Tool (free) | Posts to |
|---|---|---|
| 1 | **YouTube Studio** (desktop): upload, then *Schedule* | YouTube Shorts |
| 2 | **Meta Business Suite**: *Create reel*, tick both accounts, then *Schedule* | **Instagram Reels + Facebook Reels in one go** |
| 3 | **TikTok Studio** (tiktok.com on desktop): upload, then *Schedule* | TikTok |

Meta Business Suite needs the Instagram account switched to a **Professional** account (Creator or Business) and linked to the Kip N Dex **Facebook Page**. That's a one-time setup in Instagram: Settings > Account type.

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
6. **AI disclosure:** Kip and Dex are clearly animated characters, so YouTube's "altered or synthetic content" label is generally not required. TikTok's AI-generated content label is a judgment call; turning it on is the safe option because the voices are synthetic.
7. **TikTok Creator Rewards** has historically paid only for videos over 1 minute. Check the current rule; if it still applies, we can render a 61 s+ TikTok cut later.

## Weekly batch routine (Sunday, about 30 minutes)

1. Review the week's 7 renders.
2. YouTube Studio: upload 7 and schedule each day's slot.
3. Meta Business Suite: create 7 Reels (Instagram + Facebook) on the same schedule.
4. TikTok Studio: upload and schedule as far ahead as it allows. Post the rest mid-week.
