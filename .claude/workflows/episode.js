export const meta = {
  name: 'episode',
  description: 'Make one Kip N Dex episode with 8 agents: fact, hooks + pre-script, definition, final script, audio, audio check, animation, final check',
  whenToUse: 'The /episode command: make, continue or redo a Kip N Dex episode. args: {episode?, topic?, mode?, hook_style?, from?, until?}',
  phases: [
    {title: 'Fact', detail: 'kipndex-fact-finder picks and verifies the fact'},
    {title: 'Hooks', detail: 'kipndex-hook-writer: hooks and the pre-script'},
    {title: 'Definition', detail: 'kipndex-script-definer: tone, highlights, claims, visuals'},
    {title: 'Final script', detail: 'kipndex-script-finalizer: edit, sign off, upload kit'},
    {title: 'Audio', detail: 'kipndex-audio-producer: tone, pauses, music, voices'},
    {title: 'Audio check', detail: 'kipndex-audio-checker: sounds human, natural gaps'},
    {title: 'Animation', detail: 'kipndex-animator: beats, props, render, final.mp4'},
    {title: 'Final check', detail: 'kipndex-final-checker: ready to upload?'},
  ],
}

// args (all optional):
//   episode: 2            which episode (a new one gets the next free number)
//   topic: "tape measure" what the owner wants the episode to be about
//   mode: "trend" | "random"         topic mode (default: tools/episode/plan_next.py)
//   hook_style: "question" | "bold"  the hook test's style (default: plan_next.py)
//   from / until: stage   start at / stop after one of STAGES (e.g. until: "finalize" to read the script first)
const STAGES = ['fact', 'hooks', 'define', 'finalize', 'audio', 'audio-check', 'animate', 'final-check']
const A = args && typeof args === 'object' ? args : {}
const from = A.from || 'fact'
const until = A.until || 'final-check'
for (const s of [from, until]) {
  if (!STAGES.includes(s)) throw new Error(`"${s}" is not a stage. Stages: ${STAGES.join(', ')}`)
}
if (A.mode && !['trend', 'random'].includes(A.mode)) throw new Error(`mode "${A.mode}" must be trend or random`)
if (A.hook_style && !['question', 'bold'].includes(A.hook_style)) throw new Error(`hook_style "${A.hook_style}" must be question or bold`)
if (STAGES.indexOf(from) > STAGES.indexOf(until)) throw new Error(`from "${from}" comes after until "${until}"`)
const want = (s) => STAGES.indexOf(s) >= STAGES.indexOf(from) && STAGES.indexOf(s) <= STAGES.indexOf(until)
let ep = A.episode ? Number(A.episode) : null
if (!ep && from !== 'fact') throw new Error('Starting after the fact stage needs an episode number, e.g. {episode: 2, from: "audio"}')

const AUDIO_ROUNDS = 3 // record and check, then up to 2 fix rounds
const FINAL_ROUNDS = 3 // final check, then up to 2 fix rounds
const pad = (n) => String(n).padStart(3, '0')
const list = (xs) => xs.map((x, i) => `${i + 1}. ${x}`).join('\n')
const results = {}

// Structured results each agent must return.
const str = {type: 'string'}
const strs = {type: 'array', items: {type: 'string'}}
const int = {type: 'integer'}
const num = {type: 'number'}
const bool = {type: 'boolean'}
const obj = (properties, required) => ({type: 'object', properties, required: required || Object.keys(properties)})
const SCHEMA = {
  fact: obj({episode: int, object: str, topic_source: str, hook_seed: str, claims: int, sources: strs, runner_ups: strs, summary: str}),
  hooks: obj({hook: str, hook_style: {type: 'string', enum: ['question', 'bold']}, formula: str, wrong_theory: str,
    shape: {type: 'object'}, words: int, lines: int, summary: str}, ['hook', 'hook_style', 'formula', 'shape', 'words', 'lines', 'summary']),
  define: obj({lines: int, words: int, deliveries: strs, lint_errors: int, lint_warnings: strs, summary: str}),
  finalize: obj({blocked: bool, block_reason: str, words: int, est_seconds: num, title: str, changed_lines: strs, lint_errors: int, summary: str},
    ['blocked', 'words', 'title', 'changed_lines', 'lint_errors', 'summary']),
  audio: obj({ok: bool, voice_seconds: num, lines_generated: strs, unclean_lines: strs, changes: strs, music: str, music_db: num, summary: str},
    ['ok', 'voice_seconds', 'unclean_lines', 'summary']),
  audioCheck: obj({
    verdict: {type: 'string', enum: ['pass', 'pass_with_notes', 'fix']},
    fixes: {type: 'array', items: obj({line: str, problem: str, fix: str})},
    listen: strs,
    summary: str,
  }),
  animate: obj({ok: bool, final: str, duration: num, gate_ok: bool, new_props: strs, moves: int, longest_still_s: num, problems: strs, summary: str},
    ['ok', 'gate_ok', 'problems', 'summary']),
  finalCheck: obj({
    verdict: {type: 'string', enum: ['ready', 'fix']},
    fixes: {type: 'array', items: obj({stage: {type: 'string', enum: ['text', 'script', 'audio', 'animation']}, what: str})},
    human_checks: strs,
    summary: str,
  }),
}

// Run one stage with its project agent (.claude/agents/<role>.md). If this session
// started before the agent files existed, the agent type isn't loaded yet: then a
// general agent reads the same file and follows it.
async function run(role, phaseTitle, task, schema) {
  const where = ep ? `episode ${pad(ep)}, folder episodes/${pad(ep)}` : 'a new episode (take the next free number)'
  const prompt = `Kip N Dex, ${where}. You are one stage of the 8-agent episode pipeline; the repo root is the current folder.\n\n${task}`
  let r = null
  try {
    r = await agent(prompt, {label: role, phase: phaseTitle, schema, agentType: role})
  } catch (e) {
    log(`${role}: agent type not loaded in this session, so it runs from .claude/agents/${role}.md`)
    r = await agent(`Your role, rules and steps are in .claude/agents/${role}.md. Read that whole file first and follow it exactly.\n\n${prompt}`,
      {label: role, phase: phaseTitle, schema})
  }
  if (!r) throw new Error(`${role} stopped without a result`)
  return r
}

function finish(status, reason) {
  const d = ep ? `episodes/${pad(ep)}` : null
  return {
    status, // ready | needs_human | paused | stopped
    reason,
    episode: ep ? pad(ep) : null,
    title: results.finalize ? results.finalize.title : null,
    files: d ? {final: `${d}/final.mp4`, preview: `${d}/preview.mp4`, upload_kit: `${d}/upload.md`, review: `${d}/review.md`, listening: `${d}/listening.md`, audio_review: `${d}/audio/audio_review.md`} : null,
    listen: results.audioCheck ? results.audioCheck.listen : [],
    human_checks: results.finalCheck ? results.finalCheck.human_checks : [],
    stages: results,
  }
}

// Record (optionally), check, and loop fixes back to the producer.
async function audioRounds(record, fixes) {
  let review = null
  for (let round = 1; round <= AUDIO_ROUNDS; round++) {
    if (record || round > 1) {
      phase('Audio')
      const task = fixes
        ? `Apply exactly these fixes to the voice track, then stop:\n${list(fixes)}`
        : 'Set the tone, pauses and music bed from the final script, then record the voices.'
      const a = await run('kipndex-audio-producer', 'Audio', task, SCHEMA.audio)
      results.audio = a
      if (!a.ok) return {verdict: 'stopped', summary: `recording failed: ${a.summary}`}
      log(`voice track: ${a.voice_seconds} s${a.unclean_lines.length ? `, no clean take for ${a.unclean_lines.join(', ')}` : ''}`)
    }
    if (!want('audio-check') && !fixes) return {verdict: 'unchecked'}
    phase('Audio check')
    const last = round === AUDIO_ROUNDS
    review = await run('kipndex-audio-checker', 'Audio check',
      `Check the voice track (round ${round} of ${AUDIO_ROUNDS}${last ? ': the last round, so say plainly if a line still fails' : ''}).`,
      SCHEMA.audioCheck)
    results.audioCheck = review
    log(`audio check, round ${round}: ${review.verdict}${review.fixes.length ? ` (${review.fixes.length} fixes)` : ''}`)
    if (review.verdict !== 'fix') return review
    fixes = review.fixes.map((f) => `${f.line}: ${f.problem} -> ${f.fix}`)
  }
  return review
}

async function main() {
  if (want('fact')) {
    phase('Fact')
    const r = await run('kipndex-fact-finder', 'Fact',
      A.topic
        ? `The owner asked for this topic: "${A.topic}". Use it if it passes every check; if it doesn't, say why and pick the best alternative.`
        : A.mode === 'trend'
          ? 'Today is a trend day: find an everyday object with a hidden story inside something trending (step 1 of your instructions). If nothing fits, use a random draw and say so.'
          : A.mode === 'random'
            ? 'Today is a random day: start from a random draw (python tools/episode/topics.py random).'
            : 'Use the topic mode from python tools/episode/plan_next.py.',
      SCHEMA.fact)
    results.fact = r
    ep = ep || r.episode
    log(`episode ${pad(ep)}: ${r.object} (${r.topic_source}; ${r.claims} claims, ${r.sources.length} sources)`)
  }
  if (want('hooks')) {
    phase('Hooks')
    const style = A.hook_style
      ? `This episode's hook style is "${A.hook_style}" (the hook test, docs/HOOK_TEST.md).`
      : 'Use the hook style from python tools/episode/plan_next.py.'
    results.hooks = await run('kipndex-hook-writer', 'Hooks', `${style} Write the hooks, choose the shape, and write the pre-script.`, SCHEMA.hooks)
    log(`hook (${results.hooks.hook_style}): "${results.hooks.hook}"`)
  }
  if (want('define')) {
    phase('Definition')
    results.define = await run('kipndex-script-definer', 'Definition', 'Turn the pre-script into script.json.', SCHEMA.define)
  }
  if (want('finalize')) {
    phase('Final script')
    const r = await run('kipndex-script-finalizer', 'Final script', 'Edit and sign off the script, then write upload.md.', SCHEMA.finalize)
    results.finalize = r
    if (r.blocked) return finish('stopped', `the editor blocked the script: ${r.block_reason || r.summary}`)
    if (r.lint_errors > 0) return finish('stopped', `the final script still has ${r.lint_errors} lint errors`)
    log(`script final: "${r.title}", ${r.words} words, about ${r.est_seconds} s`)
  }
  if (want('audio') || want('audio-check')) {
    const review = await audioRounds(want('audio'), null)
    if (review.verdict === 'stopped') return finish('stopped', review.summary)
    if (review.verdict === 'fix') return finish('needs_human', `the audio still fails after ${AUDIO_ROUNDS} rounds: ${review.summary}`)
  }
  if (!want('animate') && !want('final-check')) return finish('paused', `stopped after "${until}" as asked`)

  let next = null // what the previous final check asked for
  for (let round = 1; round <= FINAL_ROUNDS; round++) {
    if ((round === 1 && want('animate')) || (round > 1 && next.rebuild)) {
      phase('Animation')
      const task = round === 1
        ? 'Write the beat sheet, add any props the story needs, and build final.mp4.'
        : [`Fix round ${round - 1} from the final check.`,
          next.audioChanged ? 'The audio changed since your last build: rebuild, and check the props still land on their words.' : '',
          next.animation.length ? `Apply these fixes:\n${list(next.animation)}` : ''].filter(Boolean).join('\n')
      const r = await run('kipndex-animator', 'Animation', task, SCHEMA.animate)
      results.animate = r
      if (!r.ok) return finish('stopped', `the build failed: ${r.summary}`)
    }
    if (!want('final-check')) return finish('paused', 'built; the final check was skipped as asked')
    phase('Final check')
    const v = await run('kipndex-final-checker', 'Final check', `Final check, round ${round} of ${FINAL_ROUNDS}.`, SCHEMA.finalCheck)
    results.finalCheck = v
    log(`final check, round ${round}: ${v.verdict}${v.fixes.length ? ` (${v.fixes.length} fixes)` : ''}`)
    if (v.verdict === 'ready') return finish('ready', v.summary)
    if (round === FINAL_ROUNDS) return finish('needs_human', `still not ready after ${FINAL_ROUNDS - 1} fix rounds: ${v.summary}`)

    // Send each fix to the stage that owns it.
    const of = (stage) => v.fixes.filter((f) => f.stage === stage).map((f) => f.what)
    let audioFixes = of('audio')
    if (of('text').length || of('script').length) {
      phase('Final script')
      const r = await run('kipndex-script-finalizer', 'Final script',
        `Fix round ${round} from the final check. Apply exactly these fixes, then stop:\n${list([...of('text'), ...of('script')])}`,
        SCHEMA.finalize)
      results.finalize = r
      if (r.blocked) return finish('stopped', `the editor blocked the script: ${r.block_reason || r.summary}`)
      if (r.changed_lines.length) audioFixes = [...audioFixes, `${r.changed_lines.join(', ')}: the words changed -> regenerate fresh`]
    }
    let audioChanged = false
    if (audioFixes.length) {
      const review = await audioRounds(true, audioFixes)
      if (review.verdict === 'stopped') return finish('stopped', review.summary)
      if (review.verdict === 'fix') return finish('needs_human', `the audio still fails after ${AUDIO_ROUNDS} rounds: ${review.summary}`)
      audioChanged = true
    }
    next = {animation: of('animation'), audioChanged, rebuild: audioChanged || of('animation').length > 0}
  }
  return finish('needs_human', 'ran out of fix rounds')
}

try {
  return await main()
} catch (e) {
  return finish('stopped', String((e && e.message) || e))
}
