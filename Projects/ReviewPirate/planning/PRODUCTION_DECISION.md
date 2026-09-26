# Production workflow decision

September 26, 2026 · Provisional; choose after an actual export test.

## Desired output

A distinctive narrated research essay, with original evidence diagrams, readable source/date labels, useful buyer decisions, and occasional visual humor. Generated scenes must never impersonate product tests. Use a pauseable buyer decision card within the video; an interactive website is unnecessary for the pilot.

The first sample must include the hook, one genuine comparison, and a transition into buyer usefulness. It must test a difficult product name, a number, a joke, captions, a source label, and one animated chart—not just a logo sting.

## Candidates

| Route | Why consider it | What must be proved | Proposed role |
|---|---|---|---|
| Original SVG/PNG graphics, scene manifest, FFmpeg assembly; licensed narration | Versionable inputs and repeatable export fit autonomous revisions | Install/runtime availability; rasterization, captions, timing, sound and visual quality | First technical spike; a small utility, not a new video editor |
| Descript Web | Script-oriented editing may make revisions easier | Sign-in, Linux browser workflow, import, actual export, plan limits, and whether agent operation is reliable | Alternative if the spike fails or owner prefers text editing |
| Shotcut | Free open-source cross-platform manual editor | Installation, timeline handoff, operator time | Human-editable fallback, not promised autonomous UI control |

[FFmpeg describes its processing capabilities](https://ffmpeg.org/about.html); [Shotcut provides its platform/features overview](https://www.shotcut.org/). [Descript documents desktop and web availability](https://help.descript.com/hc/en-us/articles/10612575375501-Troubleshooting-issues-with-installing-Descript). These establish candidate capabilities, not a tested workflow in this environment.

Do not add CapCut, Canva, Figma or a generative-video subscription just to fill a stack diagram. Existing SVGs are a starting point. Add a tool only when a specific production obstacle earns its cost.

## Voice and budget

Compare two licensed AI voices using the same 20–30-second passage. Record intelligibility, pronunciation, pacing, dry humor, listener fatigue, and revision effort. Use a pronunciation sheet and generate section-sized tracks. Owner narration remains an alternative if desired; it introduces a real recording dependency.

[ElevenLabs Starter](https://elevenlabs.io/pricing) displayed $6/month with commercial license on September 26. This is a candidate entry point, not a guarantee that its quota covers all revisions. Confirm the account plan, voice usage rights and chosen model before generation. Never put credentials in Git or ask for secrets in chat.

Proposed total incremental pilot ceiling: $30, including subscriptions and generation. This is a discussion default, not spending authorization. Record quotes separately from actual costs; stop paid generation before the agreed ceiling. Default to no incremental spending until approved. If access is unavailable, deliver the script, storyboard and local visual work and state the missing dependency; do not call a silent slideshow a finished narrated sample.

## Local feasibility finding

In the inspected shell, Python 3 and Node are on PATH. FFmpeg, ffprobe, Shotcut, Kdenlive, espeak and Chromium are not. This is a PATH observation, not a claim that all host/runtime locations were searched. Browser-control tools are available separately. No ElevenLabs or Descript connection has been verified. The execution session should check permitted bundled/local runtimes before installing dependencies and should not assume a native editor can be automated.

## Bounded sample test

1. Spend up to 60 active minutes proving that one scene, a supplied audio track and captions can become a playable MP4 with the proposed render route. Record command, versions and output. This is a feasibility timebox, not permission to ship an unattractive result.
2. If blocked, diagnose once and test the Descript Web route if an account is available. Record the exact manual dependency if neither route works. Continue independent research/script work.
3. Build the 60–90-second editorial sample from checked claims. Record agent active time, owner time, paid usage and rework separately.
4. Inspect the full sample at ordinary playback speed with sound. Check pronunciation, audio clipping, sync, small-screen text, visual pacing, source legibility and whether the viewer receives the promised insight. Automated metadata checks supplement listening/viewing.
5. Choose the stack from demonstrated quality, reproducibility, cost and operator time. Keep editable source assets and scene timings. A simple successful render wins over a longer tool comparison.

## Asset and release discipline

Keep an asset manifest: ID, source URL, creator, license/permission or proposed use basis, attribution, duration, transformations, and clearance status. Prefer original diagrams and cleared assets. Attribution alone does not establish reuse rights; flag unresolved footage for replacement or explicit review. Do not place full third-party transcripts, articles, paid assets or credentials in the open repository.

At release, check current YouTube policies and affiliate/disclosure requirements from primary sources; do not treat the old policy notes as permanent. Store large renders using an agreed artifact location and link them from GitHub rather than bloating the text repository. Public upload remains a later owner decision.
