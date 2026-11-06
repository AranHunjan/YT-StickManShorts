# Kip N Dex: account setup

Four accounts, one brand: the same name, handle, picture and one-liner everywhere. Set each one up once with the checklists below. After that, every upload takes a few minutes, because the pipeline writes all the text (`episodes/NNN/upload.md`). How to post and schedule is in [PUBLISHING.md](PUBLISHING.md).

Checked on 2026-11-06. Platforms move their menus around, so a menu name here may be slightly different.

## 1. Before you start (all four)

- [ ] **A brand email.** A free Gmail just for the channel. Use it as the contact email everywhere, so business offers don't land in your personal inbox.
- [ ] **2-step verification on all four accounts**, with an authenticator app rather than SMS. Save each platform's backup codes in a password manager. Channels get hijacked through stolen logins.
- [ ] **Never share a password.** Give your brother his own access:
  - YouTube Studio: Settings > Permissions, as Manager;
  - Facebook: Meta Business Suite, Settings > People.
  - Instagram and TikTok have no team access without the Meta link or a business setup, so keep those logins in the password manager.
- [ ] **The same everywhere:** name **Kip N Dex**, handle **@KipNDex**, and the profile picture `docs/branding/kipndex-avatar-800.png`.

## 2. Profile text (copy and paste)

| Where | Limit | Text |
|---|---|---|
| TikTok bio, Facebook Page bio | 80 | `Kip's sure he knows. Dex has the receipts. Hidden stories of everyday things 🧐` |
| Instagram name field (searchable) | 64 | `Kip N Dex \| Everyday Things Explained` |
| Instagram bio | 150 | `Kip is sure he knows how the world works. Dex has the receipts. 🧐` / `The hidden stories of everyday things, one Short a day.` / `Facts checked twice ✅` (three lines) |
| YouTube description | 1,000 | Below, under YouTube |

## 3. YouTube (YouTube Studio, on a computer)

**Customization > Branding**

| File (in `docs/branding/`) | Where it goes |
|---|---|
| `kipndex-avatar-800.png` | **Picture**. Kip peering through a magnifying glass, on Dex teal. It was picked after testing variants circle-cropped at 32 to 260 px in dark and light mode (`docs/review/avatar-comparison.png`). Alternates are in `alternatives/` |
| `kipndex-banner-2560x1440.jpg` | **Banner image**. Everything readable sits in the 1235x338 centre that shows on every device |
| `kipndex-avatar-800.png` (again, optional) | **Video watermark** (shows on long-form videos only) |

**Customization > Basic info**

- [ ] Description:

  ```text
  Kip is sure he knows how the world works. Dex has the receipts.

  Every day, one short animated story about the hidden history, science and nature behind the everyday things around you.

  Every fact is checked against two independent sources, listed under each video. Spot a mistake? Tell us in the comments and we'll pin the correction.

  A new Short every day.
  ```

- [ ] Links: Instagram, TikTok and the Facebook Page. The first one shows on the channel header.
- [ ] Contact info: the brand email.

**Customization > Layout**

- [ ] Put a **Shorts** section at the top of the home tab.

**Settings > Channel**

- [ ] Basic info: your **country of residence** (needed for the Partner Program and tax forms), and the keywords: `facts, did you know, everyday things, history, science, nature, explained, animation, stick figure, kip n dex`.
- [ ] Advanced settings: audience **"No, set this channel as not made for kids"**. The channel is for teens and adults (PLAN 1.4).
- [ ] Feature eligibility: verify with a phone number. This unlocks the intermediate features.

**Settings > Upload defaults**

- [ ] Category: **Education**. Language: **English**. Made for kids: **No**.
- [ ] Tags: the channel keywords above.
- [ ] Comments: **hold potentially inappropriate comments for review**.
- [ ] Description template:

  ```text
  {{one-line hook}}

  Sources:
  1. {{source 1}}
  2. {{source 2}}

  #shorts #facts #kipndex
  ```

**Settings > Community**

- [ ] Blocked words: common spam ("crypto", "telegram", "whatsapp", "giveaway"), plus anything that shows up later.
- [ ] Turn on holding comments with links for review. Spam bots post links.

**Settings > Permissions**

- [ ] Invite your brother as **Manager**.

**Content > Playlists**

- [ ] Create four playlists: **Kitchen & Food**, **Around the House**, **Tech & Gadgets**, **Out & About**. Each `upload.md` names the episode's playlist. Playlists keep viewers watching one Short after another.

## 4. Instagram (in the app)

- [ ] Switch to a **Creator** account: Settings and activity > Account type and tools > Switch to professional account > Creator, category **Education** (or Digital creator).
  - Creator rather than Business: the reach is the same, and Business gets a smaller music library. Our music is our own anyway, and we need none of Business's features.
- [ ] **Link the Facebook Page** (optional): Settings > Accounts Center > Accounts > add the Kip N Dex Page. Linked, Meta Business Suite posts each Reel to both at once. It was refused on our account (2026-11-06), so for now Instagram is posted from its own app ([PUBLISHING.md](PUBLISHING.md)). Account Status in the settings shows any restriction.
- [ ] Edit profile:
  - the name field and bio from section 2;
  - the link: `https://www.youtube.com/@KipNDex`;
  - the avatar.
- [ ] Contact options: the brand email.
- [ ] Privacy: keep the account public. Allow remixing.

## 5. Facebook Page

- [ ] Name **Kip N Dex**; username **@KipNDex**.
- [ ] Profile picture: the avatar.
- [ ] Cover photo: `docs/branding/kipndex-facebook-cover-1640x924.png`. It's made for the Page: it fits both the computer and the phone crops, and nothing important sits under the profile picture.
- [ ] Categories: **Video creator** and **Education**.
- [ ] Bio: the 80-character one from section 2. Links: YouTube, Instagram, TikTok. Contact: the brand email.
- [ ] Action button: **Follow**, to keep people on Facebook.
- [ ] Meta Business Suite (business.facebook.com):
  - Settings > People: add your brother.

## 6. TikTok (in the app)

- [ ] **Keep it a personal account.** Don't switch to a Business account: TikTok's Creator Rewards, which pays for videos over 1 minute like ours, is only open to personal accounts. TikTok Studio and the creator tools work on personal accounts.
- [ ] Edit profile: name **Kip N Dex**, username **kipndex**, the bio from section 2, the avatar.
- [ ] The website link in the bio unlocks on personal accounts once the account qualifies. Add the YouTube channel when it does.
- [ ] Privacy: public. Allow comments, duets and stitches (they spread videos). Comment filters: turn on keyword filtering with the same spam words as YouTube.
- [ ] Post from **TikTok Studio** on a computer (tiktok.com/tiktokstudio): full quality, and scheduling.

## 7. Every upload

The pipeline makes everything below in `episodes/NNN/`. `upload.md` has the titles, descriptions with sources, captions, hashtags, first comments and settings. The build adds `cover.jpg` and `captions.srt`.

| Step | YouTube | Instagram + Facebook | TikTok |
|---|---|---|---|
| Video | `final.mp4` | `final.mp4` | `final.mp4` |
| Text | Title and description | Caption | Caption |
| Cover | The frame named in `upload.md`, if the app offers a choice | Upload `cover.jpg` | Pick the frame named in `upload.md` |
| Subtitles | Upload `captions.srt` (Studio > Subtitles) | Facebook: upload `captions.srt` if offered, else turn on auto captions | Turn on auto captions |
| AI label | Altered or synthetic content: **No** | AI label: **on** | AI-generated content: **on** |
| After posting | Pin the comment from `upload.md`; set the related video and the playlist | Post the sources as the first comment | Post the sources as the first comment |

Instagram and Facebook are posted separately while they aren't linked: the same caption, cover and first comment on both.

Then:
- in the first hour, reply to a few comments: early replies tell each platform people are talking;
- 7 days later, add the numbers to `analytics/performance.csv` (`analytics/README.md`).

Why the subtitles file: automatic captions mishear words. Our own transcription check heard "ketchup" as "catch up" in episode 001. Our file has the script's exact words, and YouTube's auto-translated subtitles start from it.

## 8. Monetization milestones (as of 2026-11-06)

| Program | What it takes |
|---|---|
| YouTube fan funding (memberships, Super Thanks) | 500 subscribers and 3 million Shorts views in 90 days |
| YouTube Partner Program (ad revenue), today | 1,000 subscribers and 10 million Shorts views in 90 days (or 4,000 watch hours in a year) |
| YouTube Partner Program, from **1 February 2027** (new channels) | 1,000 subscribers and **20 million** Shorts views in 90 days (or 8,000 watch hours in a year). Channels already in the program keep their status |
| TikTok Creator Rewards | A personal account, 18+, 10,000 followers, 100,000 views in the last 30 days, videos over 1 minute, in a country where it's offered |
| Instagram, Facebook | Check Professional dashboard > Monetization. Meta's programs change often, and some are invite-only |

Sources: YouTube's August 2026 update, as quoted from the Help Center in [PPC Land](https://ppc.land/new-youtube-creators-face-8-000-hour-bar-for-ad-revenue-from-february-2027/); TikTok's Creator Rewards rules on TikTok Support and its Creator Academy; personal vs Business accounts: [Hootsuite](https://blog.hootsuite.com/tiktok-business-vs-personal). Check each platform's own pages before relying on a number.

## Files and how to remake them

- Avatar and banner: from `packages/animator`, run `npx remotion still src/index.ts ChannelAvatar` or `ChannelBanner`. Name, handle and tagline live in `src/style/brand.ts`.
- Facebook cover: cropped from the banner. From `docs/branding/`, run `ffmpeg -y -i kipndex-banner-2560x1440.jpg -vf "crop=2100:1182:230:129,scale=1640:924:flags=lanczos" kipndex-facebook-cover-1640x924.png`.
- An episode's `cover.jpg` and `captions.srt`: `python tools/episode/upload_files.py N`.

**Domain:** `kipndex.com` was unregistered on 2026-11-05. Buy it once there's revenue.
