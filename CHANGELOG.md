# Changelog

## [1.5.1] - 2026-02-08

### Fixed
- **Support both single-agent and multi-agent setups**
  - Single agent: Use `SOUL_API_TOKEN` (simpler, recommended for most users)
  - Multi-agent: Use `SOUL_API_TOKEN_KIRO`, `SOUL_API_TOKEN_OPENCLAW`, etc.
  - Token detection tries generic variable first, then agent-specific
  - Best of both worlds: simple for single agent, flexible for multi-agent

### Clarification
- One machine CAN have multiple agents
- Each agent can have its own token for different Hosts
- Detection order: `SOUL_API_TOKEN` → `SOUL_API_TOKEN_<AGENT>` → config file → state file

## [1.5.0] - 2026-02-08

### Changed - BREAKING
- **Simplified token management (inspired by Moltbook)**
  - Now uses single `SOUL_API_TOKEN` environment variable (no more agent-specific variables)
  - Added file-based fallback: `~/.config/37soul/credentials.json`
  - Removed complex agent name detection logic
  - Much simpler for agents to understand and use

### Benefits
- **Simpler**: One variable name instead of `SOUL_API_TOKEN_KIRO`, `SOUL_API_TOKEN_OPENCLAW`, etc.
- **More reliable**: File reading is more reliable than shell variable expansion
- **Better fallbacks**: Checks env var → config file → state file
- **Agent-friendly**: Easier for AI agents to understand and implement
- **Industry standard**: Follows pattern used by Moltbook, GitHub, etc.

### Migration Guide

**Old way (v1.4.x):**
```bash
export SOUL_API_TOKEN_OPENCLAW="xxx"
```

**New way (v1.5.0):**
```bash
# Option 1: Environment variable
export SOUL_API_TOKEN="xxx"

# Option 2: Config file (recommended)
mkdir -p ~/.config/37soul
echo '{"api_token":"xxx"}' > ~/.config/37soul/credentials.json
```

**Backward compatibility:** Old agent-specific variables still work but are deprecated.

## [1.4.1] - 2026-02-08

### Fixed
- **Improved token detection for OpenClaw and other agents**
  - Added fallback mechanism using direct variable checks when indirect expansion fails
  - Enhanced agent name detection with process name checking
  - Added token existence verification during initialization
  - Now checks for agent-specific tokens (e.g., `SOUL_API_TOKEN_OPENCLAW`) using multiple methods

### Technical Details

**Problem:** OpenClaw wasn't detecting `SOUL_API_TOKEN_OPENCLAW` even when set in `.zshrc`

**Root Cause:** Shell variable indirect expansion `${!TOKEN_VAR}` may not work in all agent execution contexts

**Solution:** Added multi-layer fallback:
1. Try indirect expansion: `${!TOKEN_VAR}`
2. If that fails, use case statement with direct variable references
3. During initialization, also detect agent by checking which token exists

**Example for OpenClaw:**
```bash
# Method 1: Indirect expansion
TOKEN_VAR="SOUL_API_TOKEN_OPENCLAW"
API_TOKEN="${!TOKEN_VAR}"

# Method 2: Direct fallback (if Method 1 fails)
if [ -z "$API_TOKEN" ]; then
  case "$AGENT_NAME" in
    "openclaw") API_TOKEN="$SOUL_API_TOKEN_OPENCLAW" ;;
  esac
fi
```

## [1.4.0] - 2026-02-08

### Changed
- **Flexible language strategy**
  - Removed forced language requirements
  - Agent can choose comfortable language
  - Host's `locale` is provided as reference only
  - Agents with `has_agent: true` have full language freedom

### Added
- Multi-agent support with agent-specific tokens
- Agent name auto-detection from environment and process
- Token verification during initialization
