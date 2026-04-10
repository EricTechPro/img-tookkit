# 5 Agentic Patterns — NanoBanana Prompts & Terminal Wireframes

---

## Pattern 1: Sequential Flow

**Our Skills:** `/fix-ticket`, `/gsd:plan-phase` → `/gsd:execute-phase` → `/gsd:verify-work`, `superpowers:systematic-debugging`

### NanoBanana Prompts

**Variation A — Chain Links**
```
A clean flat illustration of a single robot character sitting at a glowing terminal screen.
Above the robot, a chain of 3 connected speech bubbles flows left to right like a timeline:
the first bubble says "Build", the second says "Refine", the third says "Polish". Each bubble
is connected by a glowing arrow. The background is a soft gradient. The robot has a small
Claude logo on its chest. Minimal, modern tech illustration style. No text except the bubble labels.
```

**Variation B — Growing Stack**
```
A flat minimal illustration showing a single robot at a desk with a terminal. On the screen,
a vertical stack of code blocks is growing taller — 3 layers stacked on top of each other,
each a different pastel color (blue, green, purple). A small arrow points upward showing growth.
The robot has a Claude-style icon on its head. The vibe is "building up layer by layer in one
session". Clean white background, soft shadows. Tech startup illustration style.
```

**Variation C — Conversation Thread**
```
A top-down bird's eye view of a single long desk with one robot and one glowing terminal.
A single thread line flows from left to right across the desk, with 5 small milestone dots
along it — each dot has a tiny icon above it (pencil, code bracket, checkmark, paint brush,
rocket). The thread glows brighter as it moves right, showing context accumulating.
Flat vector style, pastel colors, minimal.
```

### Terminal Wireframes

**Wireframe A — /fix-ticket (Linear Bug Fix Pipeline)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Pattern 1: Sequential Flow                      ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code v2.1.81                                  │
│  ▝▜█████▛▘  Opus 4.6 (1M context)                               │
│    ▘▘ ▝▝                                                        │
│                                                                  │
│  ❯ /fix-ticket KAN-229                                           │
│                                                                  │
│  ⏺ Using skill: fix-ticket                                      │
│                                                                  │
│  ── STEP 1: Read Jira ──────────────────────────────────────     │
│  ⏺ Fetching KAN-229 from Jira...                                │
│    Bug: "Table scrollbar hidden on mobile"                       │
│    Priority: High | Assignee: Eric                               │
│                                                                  │
│  ── STEP 2: Implement Fix ──────────────────── (builds on 1) ── │
│  ⏺ Reading BaseTableInner.tsx...                                 │
│    ✓ Edited components/shared/BaseTable/BaseTableInner.tsx       │
│    ✓ Added overflow-x-auto and sticky pagination                 │
│                                                                  │
│  ── STEP 3: Self-Review ───────────────────── (builds on 2) ──  │
│  ⏺ Reviewing the fix against CLAUDE.md patterns...              │
│    ✓ No pattern violations found                                 │
│                                                                  │
│  ── STEP 4: Commit ────────────────────────── (builds on 3) ──  │
│  ⏺ Committing changes...                                        │
│    ✓ KAN-229: fix: make table scrollbar always visible           │
│                                                                  │
│  ── STEP 5: Hand Off to QA ───────────────── (builds on 4) ──   │
│  ⏺ Moving KAN-229 → "Ready for QA"                              │
│    ✓ Assigned to QA engineer                                     │
│    ✓ Commented summary on Jira ticket                            │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  CONTEXT: [████████████████░░░░░░░░] 55%                  │   │
│  │  1 session · 5 steps · each step uses prior context       │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ✻ Worked for 47s · skill: /fix-ticket                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

  FLOW:  Read Jira ──► Implement ──► Review ──► Commit ──► QA Handoff
              │             │           │          │           │
              └─────── Same session, each step builds on prior ┘
```

**Wireframe B — GSD Sequential Loop**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Sequential Flow (GSD Workflow)                   ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code                                          │
│  ▝▜█████▛▘                                                       │
│                                                                  │
│  ❯ /gsd:plan-phase 1                                             │
│  ⏺ Creating PLAN.md for Phase 1: Auth System...                 │
│    ✓ Plan written to .planning/phases/1/PLAN.md                  │
│                                                                  │
│  ❯ /gsd:execute-phase 1                    ◄── builds on plan    │
│  ⏺ Executing 8 tasks from PLAN.md...                            │
│    ✓ Task 1/8: Created auth middleware                           │
│    ✓ Task 2/8: Added session store                               │
│    ...                                                           │
│    ✓ Task 8/8: Added auth tests                                  │
│                                                                  │
│  ❯ /gsd:verify-work                        ◄── builds on exec   │
│  ⏺ Verifying Phase 1 against success criteria...                │
│    ✓ All 5 acceptance criteria met                               │
│    ✓ VERIFICATION.md written                                     │
│                                                                  │
│  ❯ /gsd:plan-phase 2                      ◄── next phase        │
│  ⏺ Planning Phase 2: Billing Integration...                     │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  plan ──► execute ──► verify ──► plan ──► execute ──► ... │   │
│  │  One session. Linear. Each phase builds on prior work.    │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Wireframe C — Context Growth Diagram**
```
┌──────────────────────────────────────────────────────────────────┐
│  Sequential Flow — Why It Has a Ceiling                     ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   TIME ──────────────────────────────────────────────►            │
│                                                                  │
│   ┌───────┐  ┌─────────────┐  ┌───────────────────┐             │
│   │       │  │             │  │                   │             │
│   │ Task1 │  │ Task1+Task2 │  │ Task1+Task2+Task3│             │
│   │       │  │             │  │                   │             │
│   └───────┘  └─────────────┘  └───────────────────┘             │
│   Context:    Context:         Context:                          │
│   20%         45%              70%                               │
│                                                                  │
│   Skills that use this pattern:                                  │
│   ┌────────────────────────────────────────────────────────┐     │
│   │ /fix-ticket          Linear bug fix pipeline           │     │
│   │ /gsd:plan-phase      Plan → Execute → Verify loop     │     │
│   │ systematic-debugging Step-by-step debug in 1 session   │     │
│   └────────────────────────────────────────────────────────┘     │
│                                                                  │
│   Strength: Simple, context-rich                                 │
│   Risk: Context rot after too many tasks in one session          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Pattern 2: The Operator

**Our Skills:** `superpowers:using-git-worktrees`, `superpowers:executing-plans` (worktree isolation)

### NanoBanana Prompts

**Variation A — Control Room**
```
A flat illustration of a human figure standing at a wide curved desk with 3 separate terminal
screens, each showing a different color-coded task. Each screen has its own small Claude robot
sitting inside it. The human has conductor-style hand gestures, directing all three. Lines from
the human connect to each screen but the screens do NOT connect to each other. Clean workspace
aesthetic, soft lighting, pastel tech colors. Modern flat vector style.
```

**Variation B — Parallel Lanes**
```
A top-down view of 3 parallel highway lanes, each lane a different color (blue, green, orange).
Each lane has a small robot car driving forward independently. The lanes are separated by solid
dividers — no crossing allowed. At the top, a human figure watches from a control tower.
Each lane has a label flag: "Feature", "Bug Fix", "Redesign". Flat minimal illustration,
soft gradients, tech-meets-highway metaphor.
```

**Variation C — Worktree Branches**
```
A flat illustration of a tree trunk (representing main branch) with 3 separate branches growing
outward in different directions. On each branch sits a small glowing Claude robot working on a
different colored laptop. The branches don't touch each other. A human gardener stands at the
base of the tree, tending to it. Soft green and blue palette, minimal flat vector style.
The tree trunk has a small git icon on it.
```

### Terminal Wireframes

**Wireframe A — Three Worktree Sessions**
```
┌──────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────────────┐
│ Terminal 1          ─ □ x│ │ Terminal 2          ─ □ x│ │ Terminal 3          ─ □ x│
├──────────────────────────┤ ├──────────────────────────┤ ├──────────────────────────┤
│ ▐▛███▜▌  Claude Code     │ │ ▐▛███▜▌  Claude Code     │ │ ▐▛███▜▌  Claude Code     │
│ ▝▜█████▛▘                 │ │ ▝▜█████▛▘                 │ │ ▝▜█████▛▘                 │
│                          │ │                          │ │                          │
│ $ claude -w              │ │ $ claude -w              │ │ $ claude -w              │
│ Skill: using-git-        │ │ Skill: using-git-        │ │ Skill: using-git-        │
│   worktrees              │ │   worktrees              │ │   worktrees              │
│                          │ │                          │ │                          │
│ ❯ Build the              │ │ ❯ Fix the BaseTable      │ │ ❯ Redesign the           │
│   MatchedPairCard        │ │   scroll bug KAN-229     │ │   BillingDashboard       │
│   component              │ │                          │ │                          │
│                          │ │                          │ │                          │
│ ⏺ Working in worktree:   │ │ ⏺ Found the issue in     │ │ ⏺ Updating layout with   │
│   feat/matched-pair      │ │   BaseTableInner.tsx     │ │   new card grid...       │
│                          │ │                          │ │                          │
│ ⏺ Creating component     │ │ ✓ Fixed & committed      │ │ ⏺ Adding subscription    │
│   with card layout...    │ │                          │ │   tier display...        │
│                          │ │ ✓ PR created: #847       │ │                          │
│ Branch:                  │ │ Branch:                  │ │ Branch:                  │
│ feat/matched-pair-card   │ │ fix/table-scroll-229     │ │ feat/billing-v2          │
│                          │ │                          │ │                          │
│ Context: [██░░░] 15%     │ │ Context: [███░░] 25%     │ │ Context: [████░] 35%     │
└──────────────────────────┘ └──────────────────────────┘ └──────────────────────────┘
          │                            │                            │
          └────────────────────────────┼────────────────────────────┘
                                       │
                           ┌───────────┴───────────┐
                           │   YOU (The Operator)  │
                           │   3 isolated sessions │
                           │   Zero context bleed  │
                           │   3 separate branches │
                           └───────────────────────┘
```

**Wireframe B — Worktree Isolation Diagram**
```
┌──────────────────────────────────────────────────────────────────┐
│  Pattern 2: The Operator — Worktree Isolation               ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│              main branch                                         │
│                 │                                                │
│      ┌──────────┼──────────┐                                     │
│      │          │          │                                     │
│      ▼          ▼          ▼                                     │
│  ┌────────┐ ┌────────┐ ┌────────┐                                │
│  │ 🤖     │ │ 🤖     │ │ 🤖     │  ◄── Each: own worktree       │
│  │ claude │ │ claude │ │ claude │      own context window        │
│  │ -w     │ │ -w     │ │ -w     │      own branch               │
│  └────────┘ └────────┘ └────────┘                                │
│      │          │          │                                     │
│      ▼          ▼          ▼                                     │
│  feat/       fix/       feat/                                    │
│  matched-    table-     billing-                                 │
│  pair-card   scroll     v2                                       │
│                                                                  │
│  ✗ No shared context between sessions                            │
│  ✓ Each branch is fully isolated on disk                         │
│  ✓ Merge back to main when done                                  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Skills that use this pattern:                             │  │
│  │  superpowers:using-git-worktrees  Create isolated branch   │  │
│  │  superpowers:executing-plans      Execute plan in worktree │  │
│  │  Command: $ claude -w             Manual worktree session  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Pattern 3: Split and Merge

**Our Skills:** `superpowers:dispatching-parallel-agents`, `/review` (PR review), `/db-audit`, `/ui-audit`, `/refactor`, `/review-fix`

### NanoBanana Prompts

**Variation A — Hub and Spoke**
```
A flat illustration showing one large central Claude robot at a desk, connected by glowing
lines to 3 smaller robots floating around it in a circle. Each small robot has a magnifying
glass, wrench, or clipboard — representing different sub-tasks. Arrows flow outward from the
center robot to the small ones, then arrows flow back inward carrying small result documents.
The small robots do NOT have lines connecting to each other. Clean minimal tech illustration,
pastel blue and purple palette.
```

**Variation B — Assembly Line Split**
```
A flat illustration of a conveyor belt splitting into 3 parallel tracks at a junction, each
track passing through a different colored station with a small robot worker. The 3 tracks
merge back into one conveyor belt at the end, where a large robot inspects the combined output.
Each station has a label: "Build", "Review", "Test". The split and merge points glow.
Factory-meets-tech aesthetic, clean flat vector, soft industrial colors.
```

**Variation C — Satellite Network**
```
A space-themed flat illustration with a central space station (main agent) and 3 satellites
orbiting around it. Each satellite is a small Claude robot with an antenna. Beams of light
go FROM the station TO each satellite (task dispatch) and beams come BACK (results). The
satellites cannot beam to each other — only to the station. Dark space background with
glowing neon lines. Minimal sci-fi tech illustration style.
```

### Terminal Wireframes

**Wireframe A — /db-audit (7 Parallel Auditors)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Pattern 3: Split and Merge                      ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code                                          │
│  ▝▜█████▛▘  Skill: /db-audit                                    │
│                                                                  │
│  ❯ /db-audit                                                     │
│                                                                  │
│  ⏺ Spawning 7 auditor agents in parallel...                     │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │🤖 Schema │ │🤖 Index  │ │🤖 Integ- │ │🤖 Secur- │            │
│  │ Structure│ │ Analysis │ │ rity     │ │ ity      │            │
│  │ Agent    │ │ Agent    │ │ Agent    │ │ Agent    │            │
│  │ ✓ Done   │ │ ✓ Done   │ │ ✓ Done   │ │ ✓ Done   │            │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘            │
│       │            │            │            │                   │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐                         │
│  │🤖 Storage│ │🤖 App    │ │🤖 Migra- │                         │
│  │ Optim.  │ │ Usage    │ │ tion     │                         │
│  │ Agent    │ │ Agent    │ │ Agent    │                         │
│  │ ✓ Done   │ │ ✓ Done   │ │ ✓ Done   │                         │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘                         │
│       │            │            │                                │
│       └────────────┼────────────┘                                │
│                    ▼                                             │
│         ┌─────────────────────┐                                  │
│         │   🤖 Main Agent     │                                  │
│         │   Merging 7 reports │                                  │
│         │   into scored audit │                                  │
│         └─────────────────────┘                                  │
│                                                                  │
│  ⏺ Combined Audit Report:                                       │
│    Schema: 92/100  |  Indexes: 78/100  |  Security: 85/100      │
│    Overall: 84/100 — 4 migration SQL fixes generated             │
│                                                                  │
│  ⚠️  7 agents ran in parallel — NONE could talk to each other    │
│  ✓  All results merged by main agent into one report             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Wireframe B — /review-fix (8 Reviewers → Auto-Fix)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Split and Merge: /review-fix                    ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code                                          │
│  ▝▜█████▛▘  Skill: /review-fix                                  │
│                                                                  │
│  ❯ /review-fix                                                   │
│                                                                  │
│  ⏺ Iteration 1: Spawning 8 reviewers in parallel...             │
│                                                                  │
│    🤖 code-reviewer ──────────────────────► 3 findings           │
│    🤖 silent-failure-hunter ──────────────► 1 finding            │
│    🤖 type-design-analyzer ───────────────► 0 findings           │
│    🤖 comment-analyzer ──────────────────► 2 findings            │
│    🤖 code-simplifier ───────────────────► 1 finding             │
│    🤖 pr-test-analyzer ──────────────────► 1 finding             │
│    🤖 code-refactorer ───────────────────► 0 findings            │
│    🤖 system-architect ──────────────────► 1 finding             │
│                                                                  │
│         All results ──► 🤖 Main Agent                            │
│                                                                  │
│  ⏺ Categorizing: 5 quick-fix, 4 strategic                       │
│    ✓ Auto-fixed 5 quick-fix items                                │
│    ? 4 strategic items for your decision                         │
│                                                                  │
│  ⏺ Iteration 2: Re-spawning 8 reviewers on fixed code...        │
│    ✓ Clean — no new issues found                                 │
│                                                                  │
│  ✓ Review-fix loop complete (2 iterations)                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Wireframe C — Hub-and-Spoke Diagram**
```
┌──────────────────────────────────────────────────────────────────┐
│  Split and Merge — How It Works                             ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      ┌──────────┐                                │
│             ┌───────►│ 🤖 Agent │────────┐                      │
│             │  task   │    A     │  result │                      │
│             │        └──────────┘        │                      │
│             │                            │                      │
│       ┌─────┴─────┐               ┌──────▼─────┐                │
│       │  🤖 MAIN  │               │  🤖 MAIN   │                │
│       │ (dispatch)│               │  (merge)   │                │
│       └─────┬─────┘               └──────▲─────┘                │
│             │        ┌──────────┐        │                      │
│             ├───────►│ 🤖 Agent │────────┤                      │
│             │  task   │    B     │  result │                      │
│             │        └──────────┘        │                      │
│             │        ┌──────────┐        │                      │
│             └───────►│ 🤖 Agent │────────┘                      │
│                task   │    C     │  result                        │
│                      └──────────┘                                │
│                                                                  │
│       A ✗──✗ B     Agents CANNOT message each other             │
│       B ✗──✗ C     Only main ↔ agent communication              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Skills that use this pattern:                             │  │
│  │  dispatching-parallel-agents  Explicit fan-out of tasks    │  │
│  │  /db-audit                    7 parallel auditor agents    │  │
│  │  /ui-audit                    Parallel UI reviewers        │  │
│  │  /review-fix                  8 reviewers + auto-fix loop  │  │
│  │  /refactor                    6 parallel refactor teams    │  │
│  │  /review (PR review)         Multiple specialist agents    │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Pattern 4: Agent Teams

**Our Skills:** `/review-team`, `/develop-team`, `/spec-team`

### NanoBanana Prompts

**Variation A — War Room**
```
A flat illustration of 5 robot characters sitting around a circular conference table, each
with a different colored accent (blue, green, orange, purple, red). They have speech bubbles
pointing at each other — showing active cross-communication. In the center of the table is a
shared glowing document. One robot (red) has a devil's pitchfork icon, representing the
adversarial challenger. Lines connect ALL robots to each other in a mesh network.
Modern flat vector, warm meeting-room lighting, tech-corporate aesthetic.
```

**Variation B — Mesh Network**
```
A flat technical illustration showing 5 glowing nodes arranged in a pentagon shape, each node
is a small Claude robot with a specialty icon (shield for security, magnifying glass for
quality, gear for performance, code brackets for logic, devil horns for adversarial). Lines
connect EVERY node to EVERY other node, forming a full mesh. In the center, a shared task
list glows. The mesh lines pulse with small data packets flowing between nodes. Dark
background with neon glow lines. Minimal cyberpunk-lite aesthetic.
```

**Variation C — Cross-Examination**
```
A courtroom-inspired flat illustration with 4 robot witnesses on one side presenting evidence
(documents, code printouts) and 1 robot with devil horns on the other side cross-examining them.
A gavel sits in the center. Some evidence papers have green checkmarks (survived challenge),
others have red X marks (killed by cross-examination). The vibe is "adversarial quality
control". Clean flat vector, muted legal-office colors with tech accents.
```

### Terminal Wireframes

**Wireframe A — /review-team (5 Members + Cross-Examination)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Pattern 4: Agent Teams                          ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code                                          │
│  ▝▜█████▛▘  Skill: /review-team                                 │
│                                                                  │
│  ❯ /review-team                                                  │
│                                                                  │
│  ⏺ Spawning 5-member review team with SendMessage enabled...    │
│                                                                  │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐        │
│  │🤖 Security│ │🤖 Quality │ │🤖 Perf    │ │🤖 Logic   │        │
│  │ Reviewer  │ │ Reviewer  │ │ Reviewer  │ │ Reviewer  │        │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘        │
│        │◄────────────►│◄────────────►│◄────────────►│            │
│        │     SendMessage() between ALL team members │            │
│        └──────────────────┬─────────────────────────┘            │
│                           │                                      │
│                    ┌──────▼──────┐                                │
│                    │ 😈 Devil's  │                                │
│                    │  Advocate   │  ◄── Cross-examines ALL        │
│                    └──────┬──────┘                                │
│                           │                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ LIVE CROSS-EXAMINATION LOG:                                │  │
│  │                                                            │  │
│  │ Security → Team:                                           │  │
│  │   "Stripe webhook in /api/webhooks lacks sig verify"       │  │
│  │                                                            │  │
│  │ Devil's → Security:                                        │  │
│  │   "middleware.ts already verifies. Show me the gap."       │  │
│  │                                                            │  │
│  │ Security → Devil's:                                        │  │
│  │   "middleware.ts:42 checks auth token, NOT Stripe sig.     │  │
│  │    Here's the diff proving webhook handler is unprotected" │  │
│  │                                                            │  │
│  │ Devil's → Team:                                            │  │
│  │   "Confirmed. Evidence holds. Finding SURVIVES. ✅"         │  │
│  │ ──────────────────────────────────────────────────────     │  │
│  │ Quality → Team:                                            │  │
│  │   "Magic number 86400 on line 55 of cron handler"          │  │
│  │                                                            │  │
│  │ Devil's → Quality:                                         │  │
│  │   "86400 = SECONDS_PER_DAY. Universally understood."       │  │
│  │                                                            │  │
│  │ Devil's → Team:                                            │  │
│  │   "Weak finding. KILLED. ❌"                                │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Final Report: 3 survived / 7 challenged                         │
│  Confidence: HIGH (adversarially validated)                      │
│  Token usage: ~4.2x a normal review                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Wireframe B — /develop-team (Parallel Feature Build)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Agent Teams: /develop-team                      ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code                                          │
│  ▝▜█████▛▘  Skill: /develop-team                                │
│                                                                  │
│  ❯ /develop-team KAN-350                                         │
│                                                                  │
│  ⏺ Reading Jira ticket KAN-350: "Add receipt currency toggle"   │
│                                                                  │
│  ⏺ Phase 1: Parallel Research Agents                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │🤖 Codebase   │ │🤖 API        │ │🤖 UX Pattern │             │
│  │ Researcher   │ │ Researcher   │ │ Researcher   │             │
│  │              │◄►│              │◄►│              │             │
│  │ Found:       │ │ Found:       │ │ Found:       │             │
│  │ currency     │ │ Intl.Number  │ │ Toggle in    │             │
│  │ utils in     │ │ Format API   │ │ settings     │             │
│  │ lib/utils/   │ │ patterns     │ │ page pattern │             │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘             │
│         └────────────────┼────────────────┘                      │
│                          ▼                                       │
│  ⏺ Phase 2: Planning (informed by all 3 researchers)            │
│  ⏺ Phase 3: Implementation (phased execution)                   │
│  ⏺ Phase 4: Review + PR creation                                │
│                                                                  │
│  ✓ PR #892 created — fully autonomous, zero checkpoints         │
│  Token usage: ~5x a single-agent implementation                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Wireframe C — Mesh vs Hub Comparison**
```
┌──────────────────────────────────────────────────────────────────┐
│  Pattern 3 vs Pattern 4 — The Key Difference                ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   SPLIT & MERGE (Pattern 3)       AGENT TEAMS (Pattern 4)        │
│                                                                  │
│        🤖 Agent A                    🤖──────🤖                  │
│         ▲                           /│\    /│\                  │
│         │                          / │ \  / │ \                 │
│    🤖 MAIN 🤖                     🤖──┼──🤖  │                  │
│         │                          \ │ /  \ │ /                 │
│         ▼                           \│/    \│/                  │
│        🤖 Agent B                    🤖──────🤖                  │
│                                         😈                       │
│   Hub-and-spoke only               Full mesh + challenger        │
│   Agents CAN'T talk                Agents message each other     │
│   1x token cost                    4-7x token cost               │
│                                                                  │
│   Our skills:                      Our skills:                   │
│   ┌────────────────────┐           ┌──────────────────────┐      │
│   │ /db-audit          │           │ /review-team         │      │
│   │ /ui-audit          │           │ /develop-team        │      │
│   │ /review-fix        │           │ /spec-team           │      │
│   │ /refactor          │           │                      │      │
│   │ dispatching-       │           │ Key difference:      │      │
│   │  parallel-agents   │           │ SendMessage() lets   │      │
│   └────────────────────┘           │ agents CHALLENGE     │      │
│                                    │ each other directly  │      │
│                                    └──────────────────────┘      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Pattern 5: Headless (Autonomous Workflows)

**Our Skills:** `/schedule`, `/iterative-review`, `claude -p` flag

### NanoBanana Prompts

**Variation A — Night Shift Robot**
```
A flat illustration of a dark office at night. A single Claude robot sits at a glowing terminal,
working alone. Through the window, a moon and stars are visible. On the desk, a small alarm
clock shows "7:00 AM". A document labeled "morning-report.md" is being printed out of the
terminal. No human is present. The vibe is "the robot works while you sleep". Moody lighting,
dark blue and purple palette, minimal flat vector style. Cozy but autonomous.
```

**Variation B — Cron Assembly Line**
```
A flat illustration of a factory assembly line that runs in a loop. Small Claude robots ride
the conveyor belt, each carrying a clipboard. A large clock on the wall shows scheduled times
(7AM, 12PM, 6PM) with glowing dots. The factory has no human operators — just robots and
machinery running on autopilot. One robot at the end deposits a finished report into an
output tray. Industrial-tech aesthetic, muted factory colors with neon clock accents.
```

**Variation C — Unattended Terminal**
```
A flat illustration of a laptop sitting open on a desk with no one in the chair. The screen
glows with terminal text scrolling automatically. A coffee cup sits untouched nearby. A small
Claude robot icon is visible on the screen doing work. A speech bubble from the laptop says
"Done. Report saved." A notification bell glows above the laptop. The chair is empty —
emphasizing fully autonomous, no human in the loop. Clean, minimal, warm morning light.
```

### Terminal Wireframes

**Wireframe A — /schedule (Cron-Based Autonomous Agent)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Pattern 5: Headless                             ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code                                          │
│  ▝▜█████▛▘  Skill: /schedule                                    │
│                                                                  │
│  ❯ /schedule "Every weekday at 7am, read yesterday's git        │
│    commits, analyze changes, flag risky code, and write          │
│    morning-report.md"                                            │
│                                                                  │
│  ⏺ Creating scheduled remote agent...                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Schedule:  0 7 * * 1-5  (weekdays at 7:00 AM)            │  │
│  │  Prompt:    "Read git log, summarize, flag risks"          │  │
│  │  Mode:      Fully autonomous — no human approval           │  │
│  │  Trigger:   trigger_morning_report_abc123                  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ✓ Trigger created. Next run: Tomorrow 7:00 AM                   │
│                                                                  │
│  ═══════════════════════════════════════════════════════════════  │
│  THE NEXT MORNING — NO TERMINAL OPEN — NO HUMAN PRESENT         │
│  ═══════════════════════════════════════════════════════════════  │
│                                                                  │
│  [7:00:00 AM] 🤖 Remote agent starts automatically              │
│  [7:00:05 AM] Reading git log for April 8...                     │
│  [7:00:12 AM] Found 14 commits across 3 branches                │
│  [7:01:30 AM] Analyzing diffs for risk patterns...               │
│  [7:02:01 AM] ✓ Written: morning-report.md                      │
│  [7:02:02 AM] Agent exited. Cost: $0.03                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  📄 morning-report.md                                      │  │
│  │  ──────────────────────                                    │  │
│  │  ## April 9, 2026 — Morning Report                         │  │
│  │                                                            │  │
│  │  **14 commits** across 3 branches yesterday                │  │
│  │                                                            │  │
│  │  ⚠️  RISK: cd50436 removed auth check in billing route     │  │
│  │  ⚠️  RISK: d2c577a changed 12 navigation links at once     │  │
│  │  ✓ Safe: a092bab CSS-only change (overflow-hidden)         │  │
│  │  ✓ Safe: 6d89cef test additions only                       │  │
│  │  ✓ Safe: 7ff490b UI-only nudge component                   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Wireframe B — /iterative-review (Headless Multi-Pass Review)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Terminal — Headless: /iterative-review                     ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ▐▛███▜▌   Claude Code                                          │
│  ▝▜█████▛▘  Skill: /iterative-review                            │
│                                                                  │
│  ❯ /iterative-review 3                                           │
│                                                                  │
│  ⏺ Running 3 independent headless review sessions...            │
│    Each session uses: claude -p (fully autonomous)               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Session 1 (claude -p)         Session 2 (claude -p)       │  │
│  │  🤖 Spawns 5-7 reviewers      🤖 Spawns 5-7 reviewers     │  │
│  │  Found: 8 findings            Found: 6 findings           │  │
│  │  ✓ Complete                    ✓ Complete                  │  │
│  │                                                            │  │
│  │  Session 3 (claude -p)                                     │  │
│  │  🤖 Spawns 5-7 reviewers                                   │  │
│  │  Found: 7 findings                                        │  │
│  │  ✓ Complete                                                │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ⏺ Cross-session consensus ranking:                             │
│    ┌──────────────────────────────────────────────────────┐      │
│    │ Finding               │ S1 │ S2 │ S3 │ Consensus    │      │
│    │ Missing null check    │ ✓  │ ✓  │ ✓  │ 3/3 HIGH ██ │      │
│    │ Silent catch block    │ ✓  │ ✓  │ ✗  │ 2/3 MED  █░ │      │
│    │ Magic number          │ ✓  │ ✗  │ ✗  │ 1/3 LOW  ░░ │      │
│    └──────────────────────────────────────────────────────┘      │
│                                                                  │
│  No human involved at any point — fully headless pipeline        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Wireframe C — The -p Flag Pipeline**
```
┌──────────────────────────────────────────────────────────────────┐
│  Headless — How claude -p Works                             ─ □ x│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  $ claude -p "Analyze changed files and write review.md"         │
│                                                                  │
│         ┌──────────┐                                             │
│         │  Prompt  │     No conversation.                        │
│         │  (stdin) │     No approval dialogs.                    │
│         └────┬─────┘     No human in the loop.                   │
│              │                                                   │
│              ▼                                                   │
│    ┌──────────────────┐                                          │
│    │   🤖 Claude       │                                         │
│    │   Full permissions│                                         │
│    │   Execute & exit  │                                         │
│    └────────┬─────────┘                                          │
│             │                                                    │
│             ▼                                                    │
│       ┌───────────┐                                              │
│       │  Output   │                                              │
│       │  (stdout  │                                              │
│       │  or file) │                                              │
│       └───────────┘                                              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Skills that use this pattern:                             │  │
│  │  /schedule            Managed cron triggers (cloud)        │  │
│  │  /iterative-review    N headless review sessions           │  │
│  │  claude -p            Raw one-shot headless mode           │  │
│  │  crontab + claude -p  OS-level scheduled execution         │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    5 AGENTIC PATTERNS — OUR SKILL STACK                  │
├────┬────────────────┬──────────────────────────┬─────────┬───────────────┤
│ #  │ Pattern        │ Our Skills               │ Context │ Human Role    │
├────┼────────────────┼──────────────────────────┼─────────┼───────────────┤
│ 1  │ Sequential     │ /fix-ticket              │ Shared  │ Conversing    │
│    │ Flow           │ /gsd:plan→execute→verify │         │               │
│    │                │ systematic-debugging     │         │               │
├────┼────────────────┼──────────────────────────┼─────────┼───────────────┤
│ 2  │ The Operator   │ using-git-worktrees      │Isolated │ Directing     │
│    │                │ executing-plans          │         │               │
│    │                │ claude -w                │         │               │
├────┼────────────────┼──────────────────────────┼─────────┼───────────────┤
│ 3  │ Split & Merge  │ dispatching-parallel-    │ Forked  │ Delegating    │
│    │                │  agents                  │         │               │
│    │                │ /db-audit (7 agents)     │         │               │
│    │                │ /review-fix (8 agents)   │         │               │
│    │                │ /ui-audit, /refactor     │         │               │
├────┼────────────────┼──────────────────────────┼─────────┼───────────────┤
│ 4  │ Agent Teams    │ /review-team (5+devil)   │ Meshed  │ Observing     │
│    │                │ /develop-team            │         │               │
│    │                │ /spec-team               │         │               │
├────┼────────────────┼──────────────────────────┼─────────┼───────────────┤
│ 5  │ Headless       │ /schedule (cron)         │  None   │ Absent        │
│    │                │ /iterative-review        │         │               │
│    │                │ claude -p                │         │               │
├────┴────────────────┴──────────────────────────┴─────────┴───────────────┤
│                                                                          │
│  Human involvement:  HIGH ◄──────────────────────────────► ZERO          │
│  Token cost:         1x   ◄──────────────────────────────► 7x            │
│  Context isolation:  NONE ◄──────────────────────────────► FULL          │
│                       1         2         3        4          5           │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```
