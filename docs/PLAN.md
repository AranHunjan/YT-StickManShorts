# YT StickMan Shorts: Master Plan

Status: planning draft, written 2026-11-05.
Numbers marked **(est.)** come from third-party reports or rough math. Check them against YouTube Studio, YouTube's Help Center, and vendor pricing pages before relying on them.

---

## 0. TL;DR

1. **Build a show, not a fact feed.** One original stickman character with a personality, a sidekick, recurring bits, and 6 to 8 rotating story formats. This keeps us on the right side of YouTube's "inauthentic content" policy, and it is the reason people come back tomorrow.
2. **Automate the production line, keep a human editor.** Research, script, voice, animation, render, and upload are all automated. A human spends about 15 minutes a day choosing the fact, approving the script, and watching the render. This is the cheapest insurance against demonetization and factual errors.
3. **Animate with code, not AI video generators.** A code-driven puppet rig plus motion graphics (Remotion). It keeps the character consistent, costs almost nothing per video, gives us full control, and does not look like "AI slop".
4. **Shorts ads alone will not pay much.** From Feb 1, 2027, Shorts ads require 10M Shorts views per 90 days, and new Partner Program applicants need 20M Shorts views per 90 days or 8,000 watch hours. Plan revenue around four streams from day one: Shorts ads, a weekly long-form episode, cross-posting to other platforms, and sponsorships.
5. **$0 cash until the channel earns its first dollar.** The only paid thing is the Claude subscription we already have.
   - **Claude Code is the brain:** research, verification, scripts, SVG props and orchestration all run there.
   - **The voice is an open-source model** running on our own computer.
   - **Everything else is free**: open-source tools and free or CC0 assets.
   - Paid upgrades come only after revenue (section 11).

---

## 1. Constraints

### 1.1 YouTube's monetization policy (the big one)

YouTube's [channel monetization policies](https://support.google.com/youtube/answer/1311392) say monetized content must "not be mass-produced, generic, repetitive, or manipulative." The policy was renamed from "repetitious content" to "inauthentic content" on July 15, 2025, and YouTube reviews the **whole channel**, so one bad pattern can demonetize everything.

**Not allowed** (quoted examples that apply directly to a stickman facts channel):

- "Videos where characters are put in the same situation over and over again with the same outcome (i.e., using a highly similar storyline template across multiple videos)"
- "Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value"
- "AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective"
- Content that "appears designed to shock or surprise viewers for the sole purpose of getting views"

**Allowed** (also quoted):

- "Same intro and outro for your videos, but the bulk of your content is different"
- "a series following a set of characters across episodes ... in which each video has a distinct storyline, focus, or concept"
- "Content that expresses your unique creative voice, like using AI to visualize a unique character and narrative you invented"
- "If you use automated tools or templates to help create your content, the final product must still demonstrate your creative vision and provide educational or entertainment value."

**AI personas on sensitive topics cannot be monetized at all**: no AI "doctor", financial adviser, or legal adviser. Our stickman never gives health, money, legal, or political advice. Facts about the body or money are fine as history or science trivia, never as "you should do this".

How the design answers each risk:

| Policy risk | Our design response |
|---|---|
| Same situation, same outcome | Format roster (section 2.3) with a scheduler that enforces variety. The character's situation and the outcome change every episode. |
| Templated slideshow / scrolling text | Every short has a narrative arc. The character acts the fact out; it is never text over stock images. |
| No creator perspective | A human editor picks and edits every episode. The character has consistent opinions and running jokes. Viewer-question episodes and replies to comments. |
| Shock for views | Hooks must be literally true and paid off. No tragedy bait, no fake disasters. |
| Mass production | One carefully made short per day, not ten. Quality over volume. |

### 1.2 Monetization thresholds and the Feb 2027 change

- **Today:** 1,000 subscribers, plus either 4,000 public watch hours in 12 months or 10M Shorts views in 90 days.
- **From Feb 1, 2027** ([Tubefilter](https://www.tubefilter.com/2026/08/10/youtube-partner-program-ad-eligibility-requirements-shorts/)):
  - New applicants need **8,000 watch hours over 365 days** or **20M Shorts views over 90 days**.
  - **Shorts ads are limited to creators with at least 10M Shorts views over 90 days**, regardless of how they qualified.
  - Existing Partner Program members are grandfathered for membership.
  - The article does not say whether the 1,000-subscriber requirement changes. Check the Help Center.
- **What this means for us:** we launch in November 2026, so we will almost certainly apply under the new rules. There are two paths:
  - Shorts path: 20M views in 90 days, about 222k views per day sustained.
  - Long-form path: 8,000 watch hours.
  - The weekly long-form episode (section 9.4) is our second path into the program, not an afterthought.
- Since August 2026, public view counts start the moment a video plays, but Partner Program eligibility still uses *qualified* views. Use Studio's numbers, not the public counter.

### 1.3 The money reality

Shorts RPM is roughly **$0.01 to $0.07 per 1,000 views globally, and $0.10 to $0.30 for US/UK-heavy audiences (est.)**. Shorts RPM is calculated on engaged views, so it is not comparable to long-form RPM.

| Monthly Shorts views | At $0.03 RPM | At $0.10 RPM |
|---|---|---|
| 3.3M (the 10M/90-day floor for Shorts ads) | ~$100 | ~$330 |
| 10M | ~$300 | ~$1,000 |
| 50M | ~$1,500 | ~$5,000 |

So diversify:

- **Long-form** earns dollars per 1,000 views, not cents (est.).
- **Cross-posting** the same render to TikTok, Instagram Reels, and Facebook Reels. Each platform has its own payout program and rules. For example, TikTok's Creator Rewards has historically required videos over 1 minute, so check current rules and render a platform-specific cut if needed.
- **Sponsorships** once the channel has a steady audience. A recognizable character is very brandable.
- **Later:** merch, licensing the character, a paid "fact archive", and translated channels.

### 1.4 Audience: build it for teens and adults, not kids

Stickman cartoons can be mistaken for kids' content. Videos that are "made for kids" get no personalized ads (much lower revenue), have comments turned off, and lose several other features. We can never mis-declare: if content is directed at children, it must be declared as such. So the channel has to be **genuinely general-audience**: adult-level humor and vocabulary, fast pacing, and topics like history, science, psychology, engineering, and nature. No nursery-style visuals or sing-song voices.

### 1.5 Every fact must be true

Fact channels die from errors: the comments fill up with "this is false", and trust and retention collapse. Every claim needs **at least 2 independent, reputable sources**, and those sources go in the description. Corrections get a pinned comment.

### 1.6 Copyright and originality

- **Original character design.** Do not imitate the look of any existing stickman series or character.
- **Music:** licensed tracks or the YouTube Audio Library only. **SFX:** CC0 or paid licenses. **Fonts:** OFL or other commercial-safe licenses.
- Keep a **license ledger** (`assets/LICENSES.md`) listing every asset and its source.
- Wikipedia text is CC BY-SA: facts are free to use, but the wording is not. Always rewrite.

### 1.7 AI disclosure

YouTube requires disclosure for *realistic* synthetic content, such as real people, altered real events, or realistic scenes. A stylized stickman generally falls outside that. The upload API supports a `status.containsSyntheticMedia` flag. Decide per video and disclose when in doubt. Never depict real people saying things they did not say.

### 1.8 YouTube API facts (checked against Google's docs, Nov 2026)

- `videos.insert` has its **own quota bucket**: 100 calls per day by default, 1 unit per call. All other endpoints share 10,000 units per day, except `search.list`, which also has its own 100-per-day bucket.
- The current `videos.insert` docs say "Videos uploaded from unverified API projects are not restricted to private viewing mode." Older docs locked such uploads to private until an audit. **Verify with one private test upload before going live.**
- `status.publishAt` supports scheduled publishing.
- **OAuth gotcha:** Google OAuth apps left in "Testing" mode issue refresh tokens that expire after about 7 days. Set the consent screen to "In production" so the daily job does not break every week.

---

## 2. Strategy: why people come back every day

### 2.1 The character

- **One original stickman** (name TBD) with a clear personality. Suggested starting point: endlessly curious, a bit overconfident, often wrong at first, then genuinely mind-blown. Viewers enjoy being one step ahead of him or learning alongside him.
- **A signature look**: one accent color and one signature accessory, kept consistent forever. This is the channel's thumbnail and brand.
- **A sidekick** (for example a deadpan pet, a talking object, or a know-it-all narrator) so episodes can have dialogue, banter, and contrast in the voices.
- **Catchphrase or signature reaction** at the "mind-blown" moment. Keep it short and use it in maybe half the episodes, not every time.

### 2.2 Habit mechanics

- **Numbered episodes** ("Fact #47") build a daily habit and a completionist urge.
- **Same publish time every day.**
- **An honest teaser of tomorrow's topic** in the last 2 to 3 seconds: a curiosity gap that pays off tomorrow.
- **Loopable endings**: the last line flows back into the first, which boosts replays.
- **Running gags and callbacks** to earlier episodes. Seasonal arcs, for example "Space Week".
- **Viewer-question episodes** answering top comments. This is great for authenticity, community, and return viewers.

### 2.3 Format roster (variety is enforced by code)

| # | Format | Structure | Example angle |
|---|---|---|---|
| 1 | The Experiment | Stickman tries something; the fact explains why it goes wrong or right | "What happens if you ..." (grounded in real science) |
| 2 | Time Traveler | Stickman lands in a historical moment and lives through the weird detail | An obscure historical rule or event |
| 3 | Myth Busted | Stickman confidently states a common belief; the sidekick takes it apart | Common misconceptions |
| 4 | Scale Shock | Motion-graphics-heavy: sizes, numbers, and timelines made visible | "How big is ... really?" |
| 5 | Become It | Stickman shrinks or turns into an animal, cell, or object for a day | Biology, physics, engineering |
| 6 | What If | A hypothetical grounded in real science, with escalating consequences | Physics and planetary science |
| 7 | The Hidden Story | An everyday object's surprising origin | Design, inventions, language |
| 8 | Viewer Question | Answering a real comment, on screen | Community-driven |

Scheduler rules:

- No format two days in a row, and no format more than twice a week.
- Rotate topic categories (science / history / nature / tech / language / space ...).
- The same "situation + outcome" pair can never repeat. Store a story signature per episode and check new ones against it.

### 2.4 Niche

Recommended positioning: **"Wild true stories behind the world you see every day"**, covering science, history, nature, engineering, and language. It is broad enough to never run out of ideas, and coherent enough to have an identity.

**Excluded topics:** health advice, finance advice, legal advice, politics, recent tragedies, and anything gory.

---

## 3. Content engine: a unique fact every day

"Random" should be **curated**, not random. A truly random Wikipedia article is usually boring. We harvest broadly, then score hard.

### 3.1 Sources

| Source | Why | Notes |
|---|---|---|
| Recent peer-reviewed research (university press releases, journals, science news) | New findings are unique by definition | Verify against the paper, not the headline |
| Wikipedia "Did you know?" archives | Thousands of already-cited surprising hooks | CC BY-SA text: rewrite, follow the citations |
| Wikipedia "Unusual articles" and similar curated lists | High surprise density | Same |
| Historical archives, "on this day", public-domain collections (Library of Congress, NASA, national archives) | Obscure, verifiable history | Good for the Time Traveler format |
| Wikidata | Hard numbers for Scale Shock | Structured, easy to cross-check |
| Viewer comments | Community questions | Feeds the Viewer Question format |

### 3.2 Pipeline

```
harvest (daily, ~50 candidates)
  -> score with rubric (cheap, can run in batch)
  -> dedupe against everything we have used or rejected (embeddings)
  -> anti-cliche filter
  -> deep verification of the top ~5 (web search + fetch, claim-level evidence)
  -> editor picks 1 of the top 3 (with sources on screen)
  -> queue (keep a buffer of ~14 verified facts)
```

### 3.3 Scoring rubric (each 1 to 5)

- **Surprise:** would 8 out of 10 adults not know this?
- **Verifiability:** at least 2 independent reputable sources?
- **Visualizability:** can a stickman act it out in 3 to 6 beats?
- **Relatability:** does it connect to the viewer's own life?
- **Story potential:** is there a twist, stakes, or a human element?
- **Safety:** not advice, not tragedy bait, not politically charged. Any failure here is an automatic reject.

### 3.4 Uniqueness and anti-cliche

- **Dedupe:** keep a one-line summary of every used *and* rejected fact in `data/facts.jsonl`.
  - At first, Claude checks each new candidate against that list. A year of daily facts easily fits in its context.
  - Once the list passes ~300 entries, add a free local embedding model (for example `all-MiniLM-L6-v2`, Apache 2.0) for a fast similarity pre-filter.
- **Cliche blocklist**, seeded with the overused "fun facts" (honey never spoils, octopuses have three hearts, Cleopatra lived closer to the Moon landing than to the pyramids, bananas are radioactive, the Emu War, and so on). Grow it over time.
- **Saturation check:** use `search.list` (100 per day) on the candidate's core idea. If the top results already have millions of views on the *same* fact, lower its score. Do not auto-reject, because a fresh angle can still win.

### 3.5 Verification

- **Claude in Claude Code** on our existing subscription. Its built-in web search and web fetch tools do the research, so there is no API key and no per-token bill.
- For every atomic claim in the script, store: the source URL, a supporting quote, and a confidence rating. Numbers must match the source exactly.
- Anything with fewer than 2 independent sources is either reworded to what the evidence actually supports, or rejected.
- **Final rule: the script may only contain claims that appear in the verified claim list.** An automated check enforces this.

---

## 4. Script and hook

### 4.1 Structure (time-coded)

| Time | Beat | Purpose |
|---|---|---|
| 0 to 2 s | **Hook**: a strong visual plus one line | Stop the swipe |
| 2 to 8 s | Setup and stakes | Why should I care? |
| 8 to 40 s | Story with 2 or 3 escalations ("but it gets weirder") | Retention |
| 40 to 52 s | Payoff / twist / the "mind-blown" moment | Satisfaction, shares |
| 52 to 58 s | Tomorrow's teaser plus a loop line | Return viewers, replays |

- **Length:** the content decides. Target 40 to 58 seconds and never pad. Shorts can now be up to 3 minutes, so 60 seconds is our creative cap, not a technical limit. Retention matters more than length.
- **Hooks:** generate about 10 hooks across pattern types (contradiction, hidden-in-plain-sight, number shock, "this was illegal", question, in-medias-res). An LLM judge scores them against a rubric, the editor picks one, and we track which pattern types perform best.
- **Honesty rule:** the hook must be literally true and paid off within the video.

### 4.2 Output format

The script writer returns **structured JSON** (Claude structured outputs, schema-validated). The beat sheet may only use actions, props, and motion-graphics components that exist in the animation manifest, so the renderer never gets a request it cannot draw.

```jsonc
{
  "episode": 47,
  "format": "time_traveler",
  "title": "...",
  "hook_pattern": "this_was_illegal",
  "claims": ["claim_id_1", "claim_id_2"],          // must exist in verified claims
  "lines": [
    {
      "id": "L1",
      "speaker": "narrator",                       // narrator | stick | sidekick
      "text": "In 1700s Russia, your beard could cost you money.",
      "delivery": "[intrigued] measured, slight smile",
      "beats": [
        {
          "action": "stroke_beard_proudly",         // from the action library
          "expression": "smug",
          "props": ["giant_beard", "tax_receipt"],
          "background": "old_town_square",
          "camera": "slow_push_in",
          "mograph": { "type": "price_tag_pop", "text": "BEARD TAX" },
          "sfx": ["paper_rustle"]
        }
      ]
    }
  ],
  "teaser": "Tomorrow: the animal that ...",
  "loop_line_connects_to": "L1",
  "description_sources": ["https://...", "https://..."]
}
```

### 4.3 Where the writing happens: Claude Code on our subscription

There is no API bill. Claude Code (included in the Claude subscription) is the writers' room and the producer. The daily flow:

1. We open Claude Code in this repo and run a project command, for example `/episode`.
2. Claude researches and verifies candidates with its built-in web search and fetch.
3. It shows us the top 3 with sources, and we pick one.
4. It writes the script JSON (validated against our schema).
5. It runs the local voice, render, and FFmpeg scripts, then shows us the preview to approve.

This also gives us the human-in-the-loop step for free.

Later, parts can run unattended with Claude Code's headless mode (`claude -p`) from a scheduler. Usage counts toward the subscription's limits. One episode a day should fit comfortably, but watch the usage meter in the first week.

When the channel earns money, the same prompts can move to the Claude API for fully unattended runs.

---

## 5. Voice (free, runs on our own computer)

There is no open-source ElevenLabs, but open-weight models are now good enough. We only need about 60 seconds of audio a day, so even slow hardware works: a model running 5x slower than real time still finishes in about 5 minutes.

**Licence rule:** the channel is monetized, so the model weights must allow commercial use.
- That rules out some popular models whose weights are non-commercial: F5-TTS, XTTS-v2 (Coqui), and Fish Speech / OpenAudio.
- Re-check the licence on the model card before adopting any model.

| Model | Licence | Strength | Hardware | Role |
|---|---|---|---|---|
| **Chatterbox / Chatterbox Turbo** (Resemble AI) | MIT | Emotion "exaggeration" dial. Turbo adds inline tags such as `[laugh]`, `[gasp]`, `[sigh]`, `[chuckle]` (English). Clones a voice from 5 to 10 s of reference audio. | NVIDIA GPU with 8 GB+ recommended; CPU and Apple Silicon work, slower | **Primary daily voice** |
| **Qwen3-TTS** (1.7B VoiceDesign) | Apache 2.0 | Designs a brand-new voice from a text description; emotion through natural-language instructions | GPU recommended | **Create the channel's original voice once**; backup daily voice |
| **Kokoro-82M** | Apache 2.0 | Tiny, fast, clean narration on any laptop CPU | CPU is fine | **Fallback** for weak hardware; little emotion control |

### How we get an original, expressive voice for $0

1. **Create the voice once.** Either:
   - design it with Qwen3-TTS VoiceDesign from a description (for example "energetic, warm, slightly raspy narrator in his late 20s, playful, fast-talking"), or
   - record 30 seconds of your own voice. You own it, and it is as authentic as it gets.
2. **Save the reference.** Keep a clean 10 to 20 second clip as `assets/voices/narrator_ref.wav`. This is the channel's voice from now on.
3. **Generate daily, line by line.** Chatterbox clones the reference for each line. Each script line carries a delivery tag (`excited`, `whisper`, `deadpan` ...), which we map to the exaggeration value and Turbo's inline tags.
4. **Give the stickman and sidekick their own voices.** Either give each its own reference clip, or pitch-shift the narrator with FFmpeg's `rubberband` filter (a free second voice, see the `ffmpeg-shorts` skill).
5. **Get word timings.** Run faster-whisper or WhisperX (open source) on the final voice track for captions, lip-sync, and beat timing.
6. **Post-process.** `mix_audio.py` in the `ffmpeg-shorts` skill does the clean-up, ducking, and -14 LUFS loudness.

### Rules and hardware

- **Never clone a real person** without their consent. Your own voice is fine.
- Wrap the TTS behind a small interface (`speak(text, voice, delivery) -> wav`) so models can be swapped.
- **No suitable GPU?** CPU is fine for 60 s a day. For heavier models, free notebook GPUs (Kaggle's weekly free GPU hours, Google Colab's free tier) can batch a week of voice at once. Check their current quotas.
- **Phase 0 bake-off:** put the same 3 script lines through each candidate, listen blind, and pick one.

---

## 6. Animation and motion graphics

### 6.1 Why a code-driven puppet instead of AI video generation

| | Procedural stickman (Remotion) | AI video models |
|---|---|---|
| Character consistency | Perfect, the same rig every time | Drifts between shots |
| Cost per 60 s | Near zero (render time only) | Significant per clip |
| Control (timing to voice, exact props, numbers on screen) | Total | Weak |
| Policy optics | Clearly an original animated character | The "AI slop" look the policy targets |
| Improves over time | Yes, the library compounds | Each clip starts from scratch |

AI image generation can still be used *occasionally* for backgrounds or props, in our fixed style and reviewed by a human, then saved into the library.

### 6.2 The stickman rig

- **Skeleton:** hip root, spine, neck, and head, plus 2-bone arms and legs with **inverse kinematics**, so hands can reach props and feet stay planted.
- **Style:** thick rounded strokes, a slightly oversized head for readability on phones, the signature accent color, and an optional subtle "boil" (hand-drawn wobble).
- **Feel:** "catchy" motion comes from animation principles: anticipation, overshoot and settle, squash and stretch on the head and body, and secondary motion. A breathing idle and blinking mean the character is never frozen.

### 6.3 Action library (start with about 25, grow to 80+)

`idle_breathe, walk, run, jump, sneak, point, shrug, facepalm, gasp_fall_back, think_chin, mind_blown, celebrate, nervous_sweat, type_laptop, read_book, carry_box, pull_rope, push_heavy, wave, slip_fall, peek_from_behind, angry_stomp, sleepy_yawn, double_take, dramatic_reveal`

Each action is a set of keyframed poses (joint angles) with easing curves, so actions can be blended, sped up, or mirrored.

### 6.4 Faces and lip-sync

- **Expressions:** neutral, happy, shocked, smug, scared, confused, angry, sleepy, determined.
- **Lip-sync:** about 6 mouth shapes (visemes) driven by the aligned word timings. A simple amplitude-driven fallback is fine for the MVP.

### 6.5 Props and backgrounds

- A curated library of flat SVG props and backgrounds in one consistent style. Start with about 150.
- **$0 sources:**
  - Claude draws simple flat SVG props in our style guide. They are free and we own them, and a human approves each one.
  - CC0 packs such as Kenney.nl.
  - Commissioned art waits until there is revenue.
- Every asset gets an entry in the manifest (name, tags, anchor points, licence), so the script writer can search for and use it.
- **Phase 3:** optional local image generation, only with a commercially licensed model (for example FLUX.1 [schnell], Apache 2.0) and a GPU. Then background removal, vectorization, and human approval. Approved props become permanent library assets.

### 6.6 Motion-graphics toolkit

- Kinetic captions: word-by-word pop with the key word highlighted.
- Number counters and odometers.
- Scale comparisons (stickman next to a blue whale, Earth next to the Sun).
- Map zooms and flight paths.
- Timelines and date flips.
- Split screens ("myth" vs "fact").
- X-ray and cutaway reveals.
- Camera moves: push, pan, whip, shake.
- Transitions: iris, whip-pan, paper tear.
- Particle bursts at the mind-blown moment.

### 6.7 Retention and pacing rules (checked automatically)

- Something on screen changes every 1.5 to 3 seconds.
- The camera is never perfectly still.
- Captions are always on, large, and high-contrast.
- **Safe zones:** keep text and faces out of the bottom ~20% and right ~15% of the frame, where the Shorts UI sits.

### 6.8 From script to render

The scene spec (the JSON in 4.2) plus the voice timings go into a **compiler** that lays out a Remotion timeline. The compiler handles:

- beats aligned to words
- action blending between poses
- prop placement at anchor points
- camera paths
- motion-graphics layers
- SFX cue points

Output: 1080x1920, 30 fps (60 fps optional), H.264 with AAC audio.

**Rendering:** locally or on a small VPS. A 60-second vertical video takes minutes on a normal CPU (est.). Remotion is free for individuals and companies of up to 3 people. Larger companies need a company licence.

---

## 7. Sound

- **Music bed** that fits the mood of each format, ducked under the voice.
  - Source: the YouTube Audio Library (free and safe on YouTube; some tracks require attribution in the description).
  - Avoid random "free music" sites, which can trigger Content ID claims.
- **SFX on every action** (whoosh, pop, boing, thud, ding). This is a big part of what makes stickman animation feel "catchy".
  - Free sources: CC0 only (Freesound filtered to CC0, Kenney audio packs).
- **Fonts:** Google Fonts (OFL).
- **Mix target:** about -14 LUFS integrated, which is around where YouTube normalizes. The voice always sits on top.
- **Tooling:** the project skill `.claude/skills/ffmpeg-shorts` handles the mix, ducking, loudness, encode, and the QA gate. Its scripts are tested.

---

## 8. QA and human review

### 8.1 Automated checks (block publishing on failure)

- Duration within the target range.
- Loudness on target, no clipping, no silent gap longer than about 0.7 seconds.
- Captions in sync with the voice. Captions inside safe zones.
- **Every claim in the script maps to a verified claim with at least 2 sources.**
- All source URLs resolve.
- Profanity and sensitive-topic scan.
- Story-signature check: this format, situation, and outcome have not been used before.
- Render sanity: no black frames, no missing assets.

### 8.2 The editor's daily routine (about 15 minutes)

1. **Pick** 1 of the top 3 verified facts, after skimming its sources.
2. **Approve** the hook and script, or edit one or two lines. This is where the human perspective comes in.
3. **Watch** the render and approve it or regenerate it.
4. **Reply** to about 10 comments, and pick tomorrow's viewer question if there is a good one.

Work 3 to 7 days ahead, so a missed day never breaks the daily streak.

---

## 9. Publishing and the growth loop

### 9.1 Upload

- `videos.insert` with:
  - title and description, with sources listed in the description
  - category "Education"
  - language set
  - `selfDeclaredMadeForKids: false` (true to the content; see 1.4)
  - `containsSyntheticMedia` set per video (see 1.7)
  - `publishAt` set to the fixed daily time
- Upload a caption file too (burned-in captions plus an uploaded track helps accessibility and search).
- Post a first comment with the sources and a question for viewers. The API can post comments; pinning may need to be done in Studio.

### 9.2 Cross-posting

Post the same master render to TikTok, Instagram Reels, and Facebook Reels, with a platform-specific cut where the rules differ. Same production cost, more revenue streams.

### 9.3 Analytics feedback loop

- Pull daily metrics:
  - YouTube Analytics API: views, engaged views, average view percentage, subscribers gained per video.
  - YouTube Studio: "viewed vs swiped away".
- Feed the results into the weights for topic category, format, and hook pattern, using a simple multi-armed bandit (Thompson sampling) so the system keeps exploring while leaning into what works.
- **Weekly human review:** what worked, what flopped, and why.
- **Do not judge the channel before about 30 episodes.** The algorithm needs time to find an audience.

### 9.4 Weekly long-form episode

An 8 to 12 minute "extended cut" built from the week's 7 stories. It adds new connective narration, deeper context, and bonus facts, and it is not a plain stitch of the shorts. It earns long-form RPM and builds watch hours toward the 8,000-hour path.

---

## 10. Architecture

```
            +-------------------+
 cron  -->  |  content-engine   |  harvest -> score -> dedupe -> verify
            +---------+---------+
                      | verified facts (DB)
            +---------v---------+
            |   script-writer   |  hooks, beats, JSON scene spec
            +---------+---------+
                      |
            +---------v---------+
            |       voice       |  TTS (2-3 voices) + forced alignment
            +---------+---------+
                      |
            +---------v---------+
            |     animator      |  Remotion: rig, actions, props, mograph, SFX
            +---------+---------+
                      | mp4 + captions
            +---------v---------+
            |     QA + review   |  automated checks, editor approves
            +---------+---------+
                      |
            +---------v---------+
            |     publisher     |  YouTube upload, schedule, cross-post
            +---------+---------+
                      |
            +---------v---------+
            |     analytics     |  metrics -> bandit weights -> content-engine
            +-------------------+
```

### Recommended stack

| Concern | Choice | Why |
|---|---|---|
| Languages | **TypeScript** for the animator (Remotion is React/TypeScript); **Python** for voice, alignment, and FFmpeg scripts | The open TTS models are Python-first |
| Rendering | Remotion (free for individuals and companies of up to 3 people) | Programmatic video, precise frame control |
| LLM / orchestration | **Claude Code on the existing subscription**: project slash commands and skills; headless `claude -p` for scheduled parts | No API bill; built-in web search and fetch; runs our local scripts |
| Fact dedupe | Claude plus `data/facts.jsonl` to start; local `all-MiniLM-L6-v2` embeddings later | Free |
| Database | JSONL files to start, SQLite later | Simple, versionable in git |
| TTS | Chatterbox (MIT), with a reference voice designed in Qwen3-TTS (Apache 2.0) or recorded by us; Kokoro (Apache 2.0) as fallback | Free, local, commercial use allowed |
| Alignment | faster-whisper or WhisperX | Word-level timing, free |
| Audio/video post | FFmpeg via the `ffmpeg-shorts` project skill | Tested scripts for mix, loudness, encode, QA |
| Scheduler | Daily `/episode` run in Claude Code; later cron (macOS/Linux) or Task Scheduler (Windows) | No server needed |
| Storage | Local disk plus a backup of `assets/` and `data/` in git | Free |
| Review UI | The preview file plus approval inside the Claude Code session; a small web page later | The 15-minute editor loop |

### Proposed repo layout

```
packages/
  content-engine/   fact sources, scoring, dedupe, verification
  script-writer/    hook generation, beat sheet, JSON schema
  voice/            TTS provider interface, alignment, post-processing
  animator/         Remotion project: rig, actions, props, mograph, compiler
  qa/               automated checks
  publisher/        YouTube upload, cross-posting
  analytics/        metrics ingestion, bandit weights
  review/           editor dashboard
assets/
  props/ backgrounds/ sfx/ music/ fonts/
  LICENSES.md       licence ledger
data/
  facts.db
docs/
  PLAN.md
```

---

## 11. Costs

### Until the first dollar: $0 cash

| Item | Cost | How |
|---|---|---|
| Research, verification, scripts, props, orchestration | $0 extra | Claude Code on the existing Claude subscription |
| Voice | $0 | Chatterbox / Qwen3-TTS / Kokoro running locally (or free notebook GPUs) |
| Word alignment | $0 | faster-whisper / WhisperX |
| Animation and rendering | $0 | Remotion (free licence tier) on our own computer |
| Audio/video post | $0 | FFmpeg |
| Music, SFX, fonts | $0 | YouTube Audio Library, CC0 SFX, Google Fonts |
| Upload and analytics | $0 | YouTube Data API and Analytics API (free quota) |
| **Total** | **$0** | Plus electricity and our time |

### Upgrades only after revenue, in order of impact

1. **Better voice, if it is the bottleneck**: a paid TTS such as ElevenLabs (est. $20 to $100 a month).
2. **Fully unattended runs**: the Claude API for the daily job (est. $30 to $40 a month at one episode a day).
3. **Commissioned art**: character sheet, prop and background packs (one-off).
4. **A small server**, so nothing depends on our computer being on (est. $10 to $40 a month).

---

## 12. Roadmap

### Phase 0, week 1: identity and pilots

- Decide the niche, the character, the sidekick, the name, and the visual style.
- Check our computer's hardware (GPU and VRAM, RAM, OS) to pick the voice model tier.
- Voice bake-off: Chatterbox vs Qwen3-TTS vs Kokoro on the same 3 lines, listened to blind.
- Create the channel's reference voice (designed, or recorded by us).
- Make **3 pilot shorts semi-manually** with the real tools to lock the style.
- Create the channel and branding. Set up the Google Cloud project and OAuth (production mode).
- **Exit when:** 3 pilots we would be proud to post.

### Phase 1, weeks 2 to 4: MVP pipeline

- Content engine with verification and the facts DB.
- Script writer producing the JSON spec.
- TTS plus alignment.
- Remotion rig with about 25 actions, 9 expressions, kinetic captions, and 5 motion-graphics components.
- Manual upload.
- **Start posting daily in week 3**, even if parts are still manual.
- **Exit when:** 7 consecutive days posted with about 30 minutes of human time a day.

### Phase 2, weeks 5 to 8: scale quality, not quantity

- Library grows to 60+ actions and 150+ props.
- All 8 formats live, plus the scheduler.
- Automated QA and the review dashboard.
- API upload with scheduling.
- Weekly long-form episode.
- **Exit when:** editor time is about 15 minutes a day and the buffer is at least 3 days.

### Phase 3, months 3 and up: growth

- Analytics bandit loop.
- Cross-posting to TikTok, Reels, and Facebook.
- Prop generator.
- Sponsorship media kit.
- Viewer-question pipeline.
- Translated or dubbed channels (Spanish, Portuguese, Hindi) reusing the same animation.

---

## 13. Risks

| Risk | Mitigation |
|---|---|
| Demonetized for inauthentic content | Character-driven narratives, format variety enforced in code, human editor, community engagement, one quality short a day |
| Factual error goes viral | 2-source rule, claim-level evidence, claim-to-script check, human review, pinned corrections |
| Shorts RPM too low | Long-form weekly episode, cross-posting, sponsorships |
| Slow start | Commit to 30+ episodes before judging; iterate hooks and formats from data |
| Classified as made for kids | Adult-level humor, topics, and pacing; general-audience design throughout |
| Music or asset claims | Licensed assets only, licence ledger |
| Policy changes | Human in the loop; assets and pipeline reusable across platforms |
| Vendor lock-in or price hikes (TTS, LLM) | Provider interfaces; store all intermediate outputs |
| Editor burnout | 15-minute daily budget, a 3 to 7 day buffer, batch review days |

---

## 14. Decisions (2026-11-05)

| Topic | Decision |
|---|---|
| Niche | **Wild true stories behind everyday things**: science, history and nature |
| Characters | Claude designs them; the owner reviews every iteration. v1 is **Kip and Dex**, see [CHARACTERS.md](CHARACTERS.md) and `docs/review/` |
| Human time | The owner reviews everything, daily |
| Budget | $0 cash until the first revenue; only the existing Claude subscription. Budget gets added if the channel takes off |
| Hosting | Everything runs on the owner's PC |
| Stack | TypeScript + Remotion for animation; Python for voice and FFmpeg |
| Languages | English first (still open: translated channels later) |

### Production PC

| Part | Spec | What it means for us |
|---|---|---|
| OS | Windows, 64-bit | PowerShell setup scripts; `uv` manages Python |
| CPU | AMD Ryzen 7 3700X (8 cores) | Remotion renders a 60 s episode in a few minutes |
| GPU | NVIDIA RTX 2070 SUPER, 8 GB | Runs Chatterbox, Chatterbox Turbo, Qwen3-TTS 1.7B (float16; Turing has no fast bfloat16) and Kokoro locally |
| RAM | 16 GB | Fine. Run one voice model at a time (the bake-off already does this) |
| Free disk | ~110 GB | Models need ~10 GB; keep at least 30 GB free for renders |

### Decided since (2026-11-05, round 2)

| Topic | Decision |
|---|---|
| Voice engine | **Chatterbox** daily (a per-line emotion dial, capped so nothing is loud); Chatterbox Turbo for fast previews and backup |
| Voices | General American for both. Calm, intriguing, never loud. Picked by measurement against research targets; see [VOICE.md](VOICE.md). Reference clips are permanent in `assets/voices/` |
| Channel name | **Kip N Dex** (YouTube **@KipNDex**, created by the owner on 2026-11-05), tagline "The hidden stories of everyday things." Setup kit: [CHANNEL.md](CHANNEL.md) |
| Watermark | Burned into every video: brand pill top-left, plus a faint handle under the characters (anti-crop). Set in `packages/animator/src/style/brand.ts` |

### Still open

1. **Claim the name everywhere:** `@kipndex` on TikTok (free on 2026-11-05) and Instagram. Upload the avatar, banner and description from [CHANNEL.md](CHANNEL.md). `kipndex.com` can wait until there is revenue.
2. **Voice review by ear:** the v2 samples in `docs/review/voice-v2/`.
3. **Pilot episode:** a verified fact, a script, voices, animation timed to the voice, the mix, and the watermark.

---

## Sources

- YouTube channel monetization policies: https://support.google.com/youtube/answer/1311392
- YouTube Data API `videos.insert`: https://developers.google.com/youtube/v3/docs/videos/insert
- YouTube Data API quota costs: https://developers.google.com/youtube/v3/determine_quota_cost
- Tubefilter, Partner Program changes from Feb 2027: https://www.tubefilter.com/2026/08/10/youtube-partner-program-ad-eligibility-requirements-shorts/
- Partner Program requirements overview (third party): https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide
- July 2026 policy clarification summary (third party): https://outlierkit.com/blog/youtube-updates-july-2026
- Shorts RPM estimates (third party, inconsistent methodology): https://joyspace.ai/youtube-shorts-rpm-2026-calculator, https://www.shortsync.app/resources/how-much-do-youtube-shorts-pay-2026
- ElevenLabs v3 (third-party overview, for the paid upgrade path): https://fal.ai/models/fal-ai/elevenlabs/tts/eleven-v3
- Remotion licence: https://www.remotion.dev/docs/license/faq
- Open-source TTS overviews (third party): https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models, https://localaimaster.com/blog/kokoro-vs-xtts-vs-chatterbox
- Chatterbox Turbo tags (third party): https://github.com/filliptm/ComfyUI_Fill-ChatterBox
- Qwen3-TTS (third party guide): https://betterstack.com/community/guides/ai/qwen3-tts/
