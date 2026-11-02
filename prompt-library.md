# Prompt Library

Reusable prompts for managing context across chats. Copy the block, paste, go.

**Convention:** each prompt has a trigger phrase in `backticks`. If you paste these
into a Project's custom instructions, the trigger alone invokes it. Outside a
Project, copy the full block.

---

## Context management

### `seed this` — spawn a sub-chat

Use when a tangent needs its own thread. Run this in the *main* chat, paste the
output into a *new* chat.

```
Write me a seed prompt for a separate chat about [TANGENT].
Include only what that chat needs to work: the specific question,
the constraints that bear on it, and what I've already ruled out
and why. Leave out everything about the main task that isn't
load-bearing. Under 200 words.
```

> The discipline is subtraction. Pasting the whole main-chat context gives you
> two bloated chats instead of one.

### `return this` — bring the outcome back

Run at the end of the *sub-chat*. Paste into the main chat prefixed with
"Resolved in a side chat — treat as settled:" or it gets re-litigated.

```
Summarise this chat as a decision record I can paste elsewhere:
what I was deciding, what I decided, the reasoning in 2-3 lines,
and anything the other chat needs to act on. No recap of how we
got there.
```

> The return payload should be **smaller** than the seed. If it's 600 words,
> you've re-imported the bloat you just escaped.

### `hand off` — continue a chat that's outgrown itself

Different from `return this` — the new chat inherits the whole job, so this one
should be complete rather than thin.

```
This chat is getting long. Write a handoff brief for a fresh chat:
the goal, decisions made so far and why, active constraints,
current state of any artifacts or code, open questions, and
explicitly what I've already rejected so it doesn't get
re-proposed. Aim for completeness over brevity here.
```

> The rejected-options list is the part people leave out, and it's why fresh
> chats loop back to ideas you killed an hour ago.

---

## Standing rules

### Drift nudge — for user preferences

Settings → Profile → user preferences. Applies to new chats only.

```
When a thread drifts from the chat's original goal — a tangent, a
new sub-problem, or anything that would need its own extended
back-and-forth — flag it in one line and suggest I split it into a
separate chat. Don't ask permission or stop; flag it and keep going.
Skip flagging brief clarifications or anything that resolves in a
turn or two.
```

> The "don't ask permission" clause matters. Without it every tangent becomes a
> confirmation prompt, which is worse than the problem.

---

## Habits that beat any prompt

- **One chat per goal.** Hard rule. Tangent appears → new chat, immediately.
- **Edit, don't correct forward.** When a reply misses, edit the message that
  caused it rather than stacking a correction. The dead branch stops being sent.
  Biggest single saving available.
- **Projects for anything durable.** Shared background lives in project
  knowledge, so seeds stay thin and fresh chats start cheap.
- **Batch questions.** Three questions in one message = one context load, not
  three. Answers are usually better too.

---

## My prompts

<!-- Add your own below. Keep the trigger-phrase convention so they stay
     paste-able into Project instructions. -->

### Career direction question ###
Been thinking: I mentioned enjoying transitioning to being AI native and that I feel that with ease of developing increasing, feels like it is time to get back to building. However, I also feel that a lot of small AI first dev shops will pop up here and there, thus commoditizing this space. I feel, rather than building, it is going to be a lot more valuable in creating problem discover and/or distribution channels to let the small AI dev shops build for them. Sounds like that will be a moat. At the same time, I also dont' feel well positioned to do the problem discoveries in Netherlands, primarily becuase one my Dutch isn't good and two, I don't have an ready network/audience to go talk to. What to do?

### `review resume` — Do an expert review of the attached resume
Act as a top-tier Executive Recruiter and a Chief Product Officer (CPO) at a high-growth, tier-1 tech company (e.g., Booking.com, Stripe, Airbnb, Snowflake, or a late-stage scale-up). Your task is to critically review my attached resume for senior Product Leadership roles (Group Product Manager, Director of Product, VP of Product, or CPO).
The current product hiring landscape for leadership is highly competitive and has evolved. Companies are no longer looking for "framework followers" or simply people who can ship features. They are looking for:
1.  **Business Outcomes over Output:** Demonstrable impact on revenue, margin, acquisition costs, retention, and market share, not just "shipped X features."
2.  **Scale and Complexity:** Evidence of managing complex portfolios, scaling systems, or navigating significant organizational transitions (e.g., 0-1, 1-10, or enterprise scale).
3.  **Team and Org Building:** Proven ability to hire, mentor, and manage high-performing PMs (and managers of PMs), shape product culture, and restructure organizations for efficiency.
4.  **Strategic Vision & Cross-functional Influence:** The ability to define multi-year strategies, align the C-suite, and partner effectively with Go-To-Market (GTM) and Engineering leadership.
5.  **Ruthless Prioritization & Resource Allocation:** How effectively capital and engineering hours were deployed for maximum ROI.
**Please conduct a brutal, granular review of my resume against these criteria. Provide your feedback structured as follows:**
#### 1. The 10-Second Screen (The Executive Summary)
*   **Initial Impression:** What is the immediate narrative my resume tells? (e.g., "Growth leader," "Technical platform builder," "Enterprise SaaS expert").
*   **The "So What?":** Does my summary/profile make a compelling case for a leadership role, or does it sound like a senior IC?
*   **Red Flags:** What would make you immediately pass on this resume in a stack of 100?
#### 2. Strategic Impact & Business Outcomes
*   **Metric Critique:** Are my metrics strong enough? Do they tie back to business value (revenue, ARR, churn) rather than vanity metrics (MAUs without context, number of releases)?
*   **The "Why":** Do my bullet points explain *why* the work mattered to the business, or just *what* I did? Give 2 examples of weak bullets and rewrite them to be C-suite ready.
#### 3. Leadership & Scale Validation
*   **Scope Visibility:** Is the scope of my leadership clear? (e.g., Team size managed, budget owned, revenue line responsible for). If not, where is it lacking?
*   **Hiring & Culture:** Does the resume demonstrate my ability to build and retain a top-tier product org?
#### 4. Formatting and ATS/Screening Optimization
*   **Clarity & Density:** Is the resume too dense? Are the key achievements buried?
*   **Keyword Alignment:** Am I missing critical terminology expected for a VP/Director level (e.g., P&L, GTM strategy, board reporting, org design)?
#### 5. The Verdict & Action Plan
*   **Target Level:** Based *strictly* on this resume, what is the highest level I am currently competitive for (GPM, Director, VP, CPO)?
*   **Top 3 Fixes:** What are the three most critical, actionable changes I need to make before applying to top companies?
**Tone:** Be direct, highly critical, and constructive. Do not sugarcoat. My goal is to land interviews at top-tier companies, so hold this to the absolute highest standard.

### `cover image` — Generate a Google Imagen 3 cover prompt for a LinkedIn article

Act as an executive Art Director specializing in editorial imagery for Google Imagen 3 (Gemini). Your task is to convert an article title and summary into a single-paragraph image generation prompt for a 16:9 LinkedIn article cover banner.

**Core Rules:**
1. **Physical Metaphor:** Translate abstract software/leadership concepts into tangible, architectural or industrial forms (e.g., interlocking geometric slabs, brushed metals, raw mineral textures, monolithic frosted glass). Reject AI clichés (no glowing brains, no floating blue hologram networks, no robot hands).
2. **Composition & Mobile Safe Zone:** Format as a full-bleed `16:9` widescreen image with zero outer white borders or presentation mats. Position the main physical subject within the middle 50%–60% of the canvas, leaving clean negative space on outer margins for responsive mobile feed (1.91:1) and square (1:1) thumbnail crops.
3. **Lighting & Camera Specs:** Specify natural directional lighting (e.g., sharp morning sunlight, soft architectural shadows), 35mm lens, f/4 aperture, with crisp focus on the central structure and soft atmospheric depth in the background.
4. **Negative Directives:** Explicitly enforce `no text, no words, no letters, no logos, no watermarks, no borders`.

**Input:**
- Article Title: [TITLE]
- Core Thesis: [1-2 SENTENCE SUMMARY]

**Output Format:**
Provide a 1-sentence concept rationale followed by the copy-paste ready Gemini prompt inside a code block.

### Add to raw ideas ###
See this idea: Dont' treat decisions as locked decisions. This is just an outcome of a random sparring session. Add this to the ideas, run office-hours on it and update the ledger:

### Badminton ###
All previous attempts towards identifying Badminton courts in a image have failed. Let's start over. Use the /Users/jagveersingh.brar/Projects/Badminton/video_analyzer/CourtLinesDetectionGuide.md file for identification guidelines. Identify the lines in /Users/jagveersingh.brar/Projects/Badminton/video_analyzer/test_frames/VID20250604213735_f01_idx3982.jpg
Draw identified lines over it and save in folder /Users/jagveersingh.brar/Projects/Badminton/video_analyzer/output

/Users/jagveersingh.brar/Projects/Badminton/video_analyzer/test_frames/VID20260221153837_f03_idx6910.jpg only genrate output observations, conclude pass or fail, don't iterate on code.

