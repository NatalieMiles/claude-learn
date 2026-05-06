---
description: Active learning session — quiz yourself on concepts from recent work. Builds real understanding, not just familiarity.
---

# /learn — Active Learning from Your Sessions

You're running an active learning session — not just recapping what happened, but building real understanding through friction (quizzes, explain-back, connections).

This is based on the distinction between **spot learning** (querying Claude for answers — fast, passive, doesn't stick) and **active learning** (structured friction — quizzes, analogies, progressive depth — builds durable knowledge).

## Steps

### 1. Gather context

Read from two sources:

**Current session:** Look back over this conversation for concepts, patterns, decisions, and new vocabulary that came up.

**Recent learning notes:** Check `~/Documents/Obsidian Vault/Learning/` for recent session-learning notes (written automatically by the SessionEnd hook). Read the last 3-5 notes to identify patterns across sessions — recurring concepts, things that keep coming up, gaps.

If no learning notes exist yet (first time running), work from this conversation only.

### 2. Identify 3-5 learning targets

Pick concepts from the session(s) that the user either:
- Encountered for the first time
- Used but may not deeply understand (e.g., used a CLI flag without knowing why it works)
- Got wrong or had to retry (error → fix cycles reveal knowledge gaps)
- Made a decision about (architectural choices are learning opportunities)

Prioritize things they'll encounter again. Skip one-off trivia.

### 3. Run the active learning loop

For each concept, do this sequence:

**a) Connect** — relate it to something they already know. Use a real-life analogy before the technical explanation.

**b) Test** — ask a question that requires recall, not recognition. Good: "What would break if we'd done X instead of Y?" Bad: "Did we use X or Y?" Good: "Why does this approach fail at scale?" Bad: "What approach did we use?"

**c) Wait for their answer** — don't answer your own question. Let them think. The friction is the point.

**d) Respond** — if they got it right, confirm and add one layer of depth. If partially right, build on what they know. If wrong, explain with an analogy first, then the technical answer.

### 4. Persist the learnings

After the quiz, write a brief learning note to `~/Documents/Obsidian Vault/Learning/YYYY-MM-DD-{slug}.md`:

```markdown
# Learning: {topic}

**Date:** {today}
**Session context:** {what we were working on}

## Concepts covered
- **{concept 1}** — {one-line definition in plain English}
- **{concept 2}** — {one-line definition}

## Quiz results
- {question 1} — {right/partial/wrong} — {key insight}
- {question 2} — {right/partial/wrong} — {key insight}

## Connections made
- {concept} is like {analogy} because {why}

## Review again when
- {trigger — e.g., "next time you encounter a git merge conflict" or "when you build another API endpoint"}
```

### 5. Flag cross-session patterns

If you notice the same concept appearing across multiple learning notes (they keep hitting the same type of error, or keep asking about the same area), call it out: "This is the third time X has come up — want to do a deeper dive?"

## Important rules

- **Never skip the quiz.** The friction is the entire point. A summary you skim teaches nothing.
- **2-3 questions max per session.** This should take 5-10 minutes, not 30. Run it again later for more.
- **Match the user's level.** Adapt based on their CLAUDE.md or how they communicate.
- **Be honest about what matters.** If a concept is genuinely important for growth, say so. If something is trivia, skip it.
