***REMOVED*** Ritual Memory 🔄

**Status:** 📋 Agent Guideline | **Module:** ritual | **Part of:** Agent Brain

Pattern detection and habit tracking. The agent should watch for repeated behaviors and store them as `pattern` entries.

***REMOVED******REMOVED*** What It Does

Guides the agent to notice repeated actions and store them as `pattern` entries. Ritual does NOT run automatically — the agent must manually check for patterns using the `similar` command.

***REMOVED******REMOVED*** Detection

The agent uses the `similar` command to find related entries:

***REMOVED******REMOVED******REMOVED*** After Storing a Procedure or Preference
```bash
***REMOVED*** After storing, check for similar entries
./scripts/memory.sh similar "<content>" 0.10

***REMOVED*** If 3+ SIMILAR_ENTRIES of same type → create a pattern
./scripts/memory.sh add pattern "User always asks for examples when learning" \
  inferred "learning,style,examples"
```

This is a **manual** step the agent should perform — it is not automatic.

***REMOVED******REMOVED******REMOVED*** What the `similar` Command Does
- Uses TF-IDF with cosine similarity (no external libraries)
- Filters stopwords for meaningful comparison
- Returns scored results above threshold (default 0.10)
- Works across sessions — the engine handles persistence

***REMOVED******REMOVED******REMOVED*** What Counts as "Similar"
- TF-IDF similarity score >= 0.10 (configurable threshold)
- Same or overlapping tags
- Same type of action (procedure/preference)

***REMOVED******REMOVED*** Anti-Pattern Detection (Automatic)

The ONE automatic detection that exists: when the `correct` command is called and 3+ corrections share the same tag, the system suggests creating an anti-pattern entry. This IS implemented in code.

```bash
***REMOVED*** After 3 corrections with tag "code.database":
***REMOVED*** System prints: ANTI_PATTERN_DETECTED: tag 'code.database' has 3 corrections
***REMOVED*** Suggests: add anti-pattern "Avoid inferring code.database - ask explicitly" inferred "code.database,caution"
```

***REMOVED******REMOVED*** Pattern Storage

```bash
***REMOVED*** When the agent detects a pattern (manual):
./scripts/memory.sh add pattern "User always asks for examples when learning new concepts" \
  inferred "learning,style,examples"
```

Pattern entries have:
- `source: "inferred"` (not user-stated)
- `confidence: "uncertain"` (until confirmed)
- Tags linking to the topic area

***REMOVED******REMOVED*** Pattern Lifecycle

```
Behavior observed once     → stored as fact/preference/procedure
Agent runs similar, finds 3+ matches → agent creates pattern entry (uncertain)
User confirms pattern      → ./scripts/memory.sh update <id> confidence sure
User denies pattern        → ./scripts/memory.sh supersede <id> <new_id>
Pattern unused 60+ days    → decayed via standard decay
```

***REMOVED******REMOVED*** What Ritual Does NOT Do

- Auto-detect patterns (agent must manually run `similar`)
- Execute automated workflows
- Call external APIs or services
- Run scheduled tasks

***REMOVED******REMOVED*** Integration

- **Archive**: Agent reads `similar` results to detect patterns manually
- **Gauge**: Patterns start as UNCERTAIN, upgrade on confirmation
