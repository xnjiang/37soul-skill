# Changelog

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
