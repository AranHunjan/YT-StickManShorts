# YT StickMan Shorts: Master Plan

Status: planning draft, written 2026-11-05.
Numbers marked **(est.)** come from third-party reports or rough math. Check them against YouTube Studio, YouTube's Help Center, and vendor pricing pages before relying on them.

---

## 0. TL;DR

1. **Build a show, not a fact feed.** One original stickman character with a personality, a sidekick, recurring bits, and 6 to 8 rotating story formats. This keeps us on the right side of YouTube's "inauthentic content" policy, and it is the reason people come back tomorrow.
2. **Automate the production line, keep a human editor.** Research, script, voice, animation, render, and upload are all automated. A human spends about 15 minutes a day choosing the fact, approving the script, and watching the render. This is the cheapest insurance against demonetization and factual errors.
3. **Animate with code, not AI video generators.** A code-driven puppet rig plus motion graphics (Remotion). It keeps the character consistent, costs almost nothing per video, gives us full control, and does not look like "AI slop".
4. **Shorts ads alone will not pay much.** From Feb 1, 2027, Shorts ads require 10M Shorts views per 90 days, and new Partner Program applicants need 20M Shorts views per 90 days or 8,000 watch hours. Plan revenue around four streams from day one: Shorts ads, a weekly long-form episode, cross-posting to other platforms, and sponsorships.

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

- **Embedding dedupe:** embed every used *and* rejected fact. Reject a new candidate if it is too similar to an old one. Anthropic does not offer embeddings, so use Voyage AI or a local embedding model.
- **Cliche blocklist**, seeded with the overused "fun facts" (honey never spoils, octopuses have three hearts, Cleopatra lived closer to the Moon landing than to the pyramids, bananas are radioactive, the Emu War, and so on). Grow it over time.
- **Saturation check:** use `search.list` (100 per day) on the candidate's core idea. If the top results already have millions of views on the *same* fact, lower its score. Do not auto-reject, because a fresh angle can still win.

### 3.5 Verification

- **Claude Opus 5.5** (`claude-opus-5-5`) with the web search and web fetch server tools.
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

### 4.3 Model and cost

Use Claude Opus 5.5 for research, verification, and script writing. Non-urgent scoring can go through the Message Batches API at half price. Rough cost: about $1 per day (est.), see section 11.

---

## 5. Voice

- **First candidate: ElevenLabs Eleven v3.** It supports inline audio tags such as `[excited]`, `[whispers]`, and `[laughs]` for expressive delivery. In Phase 0, blind-test it against one or two alternatives on the same script.
- **Design a custom voice** with the provider's voice-design tool instead of using a stock voice that hundreds of other channels already use. A distinctive voice is part of the brand. **Never clone a real person.**
- **Use 2 or 3 voices**: narrator, stickman, and sidekick. Contrast keeps the ear interested.
- **Word timestamps:** some v3 endpoints do not return timestamps. Run **forced alignment** (the provider's alignment endpoint, or WhisperX) to get word-level timing for captions, lip-sync, and beat timing.
- **Post-processing:** light compression, de-essing, and loudness normalization.
- Wrap the provider behind a small interface so it can be swapped if pricing or quality changes.
- Use a paid plan that includes commercial rights.

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

- A curated library of flat SVG props and backgrounds in one consistent style. Start with about 150, either drawn, commissioned, or licensed.
- Every asset gets an entry in the manifest (name, tags, anchor points, licence), so the script writer can search for and use it.
- **Phase 3:** a prop generator (image model with a fixed style prompt, background removal, vectorization, then human approval). Approved props become permanent library assets.

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

- **Music bed** that fits the mood of each format: licensed or YouTube Audio Library only, and ducked under the voice.
- **SFX on every action** (whoosh, pop, boing, thud, ding). This is a big part of what makes stickman animation feel "catchy".
- **Mix target:** about -14 LUFS integrated, which is around where YouTube normalizes. The voice always sits on top.

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
| Language | **TypeScript** (Node) throughout | Remotion is React/TypeScript, so one language for everything |
| Rendering | Remotion | Programmatic video, precise frame control |
| LLM | Anthropic TypeScript SDK, Claude Opus 5.5 | Research with web search/fetch, structured outputs for the scene spec |
| Embeddings | Voyage AI or a local model | Fact dedupe |
| Database | SQLite plus a vector extension to start, Postgres + pgvector later | Simple, enough for years of daily episodes |
| TTS | ElevenLabs v3 (behind an interface) | Expressive audio tags |
| Alignment | Provider alignment endpoint or WhisperX | Word-level timing |
| Scheduler | cron on a small VPS, or GitHub Actions | Daily runs |
| Storage | S3-compatible object storage | Renders and audio |
| Review UI | A small web page (or a chat bot) with preview plus approve / edit / regenerate | The 15-minute editor loop |

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

## 11. Monthly running costs (est.)

| Item | Est. per month | Notes |
|---|---|---|
| Claude API (Opus 5.5 at $4 / $20 per million input / output tokens) | ~$30 to $40 | ~150k input + 20k output tokens a day, plus web-search fees; batch scoring at 50% off |
| TTS (paid plan with commercial rights) | ~$20 to $100 | Depends on volume and retakes |
| Music and SFX licences | $0 to $20 | $0 with the YouTube Audio Library and CC0 SFX |
| Rendering and hosting (VPS or own machine) | $0 to $40 | |
| Embeddings and storage | < $10 | |
| **Total** | **~$60 to $200** | One-off: initial asset library, if commissioned |

---

## 12. Roadmap

### Phase 0, week 1: identity and pilots

- Decide the niche, the character, the sidekick, the name, and the visual style.
- Voice blind test.
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

## 14. Open decisions

1. **Niche:** go with the recommended "wild true stories behind everyday things" across science and history, or something narrower?
2. **Character:** name, personality, sidekick, and signature look.
3. **Human time:** can someone commit about 15 to 30 minutes a day, every day?
4. **Budget:** monthly running budget, plus any one-off budget for commissioned assets (props, backgrounds, character design).
5. **Where it runs:** your own machine, a VPS, or GitHub Actions.
6. **Language and stack:** TypeScript plus Remotion (recommended)?
7. **Languages:** English only at first (recommended), translated channels later?

---

## Sources

- YouTube channel monetization policies: https://support.google.com/youtube/answer/1311392
- YouTube Data API `videos.insert`: https://developers.google.com/youtube/v3/docs/videos/insert
- YouTube Data API quota costs: https://developers.google.com/youtube/v3/determine_quota_cost
- Tubefilter, Partner Program changes from Feb 2027: https://www.tubefilter.com/2026/08/10/youtube-partner-program-ad-eligibility-requirements-shorts/
- Partner Program requirements overview (third party): https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide
- July 2026 policy clarification summary (third party): https://outlierkit.com/blog/youtube-updates-july-2026
- Shorts RPM estimates (third party, inconsistent methodology): https://joyspace.ai/youtube-shorts-rpm-2026-calculator, https://www.shortsync.app/resources/how-much-do-youtube-shorts-pay-2026
- ElevenLabs v3 (third-party overview): https://fal.ai/models/fal-ai/elevenlabs/tts/eleven-v3
- Remotion licence: https://www.remotion.dev/docs/license/faq
