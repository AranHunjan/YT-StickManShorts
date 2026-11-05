# Kip N Dex: channel setup

- **YouTube:** https://www.youtube.com/@KipNDex (created 2026-11-05)
- **Claim the same handle on:** TikTok (`@kipndex` was free on 2026-11-05) and Instagram (check by hand).
- **Domain:** `kipndex.com` was unregistered on 2026-11-05. Buy it once there's revenue.

## Files (in `docs/branding/`)

| File | Where it goes in YouTube Studio |
|---|---|
| `kipndex-avatar-800.png` | Customization > Branding > **Picture** (800x800; YouTube crops it to a circle, and everything important is central) |
| `kipndex-banner-2560x1440.jpg` | Customization > Branding > **Banner image**. Everything readable sits in the 1235x338 centre that shows on every device |
| `kipndex-avatar-800.png` (again, optional) | Customization > Branding > **Video watermark** (shows on long-form videos) |

To regenerate them after a change: from `packages/animator`, run `npx remotion still src/index.ts ChannelAvatar` or `ChannelBanner`. Name, handle and tagline live in `src/style/brand.ts`.

## Description (Customization > Basic info)

```text
Kip is sure he knows how the world works. Dex has the receipts.

Every day, one short animated story about the hidden history, science and nature behind the everyday things around you.

Every fact is checked against two independent sources, listed under each video. Spot a mistake? Tell us in the comments and we'll pin the correction.

A new Short every day.
```

## Upload defaults (Settings > Upload defaults)

- **Category:** Education
- **Made for kids:** No. The content is made for a general teen and adult audience; see PLAN 1.4.
- **Description template:**

```text
{{one-line hook}}

Sources:
1. {{source 1}}
2. {{source 2}}

#shorts #facts #kipndex
```

## Channel keywords (Settings > Channel > Basic info)

`facts, did you know, everyday things, history, science, nature, explained, animation, stick figure, kip n dex`
