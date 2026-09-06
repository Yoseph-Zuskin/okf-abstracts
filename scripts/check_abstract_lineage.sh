#!/usr/bin/env bash
# OKF Abstract Lineage Checker (bash version)
#
# Checks if abstract entities have changed since concept verification.
# Compares concept generated.at/verified.at timestamps against abstract entity git history.
#
# Usage: ./check_abstract_lineage.sh <bundle-path> [--abstracts-repo <path>]
#
# Dependencies: bash, git, date (GNU or BSD), grep, awk

set -euo pipefail

# Colors for output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Default values
BUNDLE_PATH=""
ABSTRACTS_REPO=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --abstracts-repo)
            ABSTRACTS_REPO="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 <bundle-path> [--abstracts-repo <path>]"
            echo ""
            echo "Options:"
            echo "  --abstracts-repo <path>   Path to local okf-abstracts repo"
            echo "  -h, --help                Show this help"
            exit 0
            ;;
        *)
            if [[ -z "$BUNDLE_PATH" ]]; then
                BUNDLE_PATH="$1"
            else
                echo "Unknown argument: $1" >&2
                exit 2
            fi
            shift
            ;;
    esac
done

# Validate bundle path
if [[ -z "$BUNDLE_PATH" ]]; then
    echo "Error: Bundle path is required" >&2
    exit 2
fi

BUNDLE_PATH=$(realpath "$BUNDLE_PATH")
if [[ ! -d "$BUNDLE_PATH" ]]; then
    echo "Error: Bundle path does not exist: $BUNDLE_PATH" >&2
    exit 2
fi

if [[ -n "$ABSTRACTS_REPO" ]]; then
    ABSTRACTS_REPO=$(realpath "$ABSTRACTS_REPO")
    if [[ ! -d "$ABSTRACTS_REPO" ]]; then
        echo "Error: Abstracts repo not found: $ABSTRACTS_REPO" >&2
        exit 2
    fi
    # Verify it's a git repo
    if [[ ! -d "$ABSTRACTS_REPO/.git" ]]; then
        echo "Error: Abstracts repo is not a git repository: $ABSTRACTS_REPO" >&2
        exit 2
    fi
fi

# Helper functions
log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

# Parse ISO 8601 timestamp to epoch seconds (cross-platform)
parse_iso_to_epoch() {
    local timestamp="$1"
    # Handle both Z and +00:00 formats
    timestamp="${timestamp/Z/+00:00}"
    timestamp="${timestamp/%+00:00/+0000}"

    # Try GNU date first
    if date -d "$timestamp" +%s 2>/dev/null; then
        return
    fi
    # Try BSD date (macOS)
    if date -j -f "%Y-%m-%dT%H:%M:%S%z" "$timestamp" +%s 2>/dev/null; then
        return
    fi
    # Fallback: try without timezone
    timestamp="${timestamp%+0000}"
    if date -d "$timestamp" +%s 2>/dev/null; then
        return
    fi
    if date -j -f "%Y-%m-%dT%H:%M:%S" "$timestamp" +%s 2>/dev/null; then
        return
    fi
    echo "0"
    return 1
}

# Extract frontmatter as YAML block
extract_frontmatter() {
    local content="$1"
    echo "$content" | awk '
        /^---$/ { if (++count == 2) exit; next }
        count == 1 { print }
    '
}

# Extract subtype_of entries (canonical key; legacy aliases accepted)
extract_subtype_versions() {
    local content="$1"
    # Extract subtype_of block
    echo "$content" | awk '
        /^(subtype_of|subtypes_of|subclass_of|subconcept_of):/ { in_block = 1; next }
        in_block && /^  - \{ type:/ {
            # Extract type and version
            match($0, /type: *([^,}]+)/, type_arr)
            match($0, /version: *([^}]+)/, ver_arr)
            if (type_arr[1] && ver_arr[1]) {
                gsub(/^ +| +$/, "", type_arr[1])
                gsub(/^ +| +$/, "", ver_arr[1])
                gsub(/^[" ]+|[" ]+$/, "", type_arr[1])
                gsub(/^[" ]+|[" ]+$/, "", ver_arr[1])
                print type_arr[1] "=" ver_arr[1]
            }
        }
        in_block && /^[^ ]/ && !/^  -/ { in_block = 0 }
    '
}

# Extract latest verified timestamp
extract_latest_verified() {
    local content="$1"
    local fm=$(extract_frontmatter "$content")
    echo "$fm" | awk '
        /^- verified:/ { in_verified = 1; next }
        /^verified:/ { in_verified = 1; next }
        in_verified && /^  - \{ by:/ {
            match($0, /at: *[^}]+/, at_arr)
            if (at_arr[0]) {
                gsub(/.*at: *['"'"'?]/, "", at_arr[0])
                gsub(/['"'"'?] *}$/, "", at_arr[0])
                gsub(/^ +| +$/, "", at_arr[0])
                print at_arr[0]
            }
        }
    '
}

# Extract generated.at timestamp
extract_generated_at() {
    local content="$1"
    local fm=$(extract_frontmatter "$content")
    echo "$fm" | awk '
        /^generated:/ { in_gen = 1; next }
        in_gen && /at:/ {
            match($0, /at: *['"'"'?]([^'"'"']+)['"'"'?]/, at_arr)
            if (at_arr[1]) {
                print at_arr[1]
                exit
            }
        }
    '
}

# Check if abstract entity has changed since timestamp
check_abstract_changed() {
    local abstract_type="$1"
    local abstract_version="$2"
    local concept_verified_epoch="$3"
    local abstracts_repo="$4"

    if [[ -z "$abstracts_repo" || ! -d "$abstracts_repo/.git" ]]; then
        return 1  # Can't check without repo
    fi

    # Find the abstract entity file in okf-abstracts repo
    local entity_file=""
    # Search in entities/ subdirectories
    while IFS= read -r -d '' file; do
        local fm=$(head -n 50 "$file" | extract_frontmatter)
        local title=$(echo "$fm" | awk '/^title:/ {sub(/^title: /, ""); gsub(/^[" ]+|[" ]+$/, ""); print; exit}')
        local type=$(echo "$fm" | awk '/^type:/ {sub(/^type: /, ""); gsub(/^[" ]+|[" ]+$/, ""); print; exit}')

        if [[ "$type" == "Class" && "$title" == "$abstract_type" ]]; then
            entity_file="$file"
            break
        fi
    done < <(find "$abstracts_repo/entities" -name "*.md" -print0 2>/dev/null)

    if [[ -z "$entity_file" || ! -f "$entity_file" ]]; then
        return 1  # Entity not found
    fi

    # Get the latest commit timestamp for this file
    local latest_commit_epoch=$(git -C "$abstracts_repo" log -1 --format="%ct" -- "$entity_file" 2>/dev/null)
    if [[ -z "$latest_commit_epoch" ]]; then
        return 1
    fi

    # Compare timestamps
    if [[ "$latest_commit_epoch" -gt "$concept_verified_epoch" ]]; then
        echo "changed"
        return 0
    fi
    return 1
}

# Main check function
check_bundle() {
    local bundle_path="$1"
    local abstracts_repo="$2"

    local warnings=0
    local concepts_checked=0

    # Find all concept and skill files
    local files=()
    while IFS= read -r -d '' file; do
        files+=("$file")
    done < <(find "$bundle_path" -type f \( -path "*/concepts/*.md" -o -path "*/skills/*/SKILL.md" \) -print0 2>/dev/null)

    for filepath in "${files[@]}"; do
        local filename=$(basename "$filepath")
        [[ "$filename" == "index.md" || "$filename" == "log.md" || "$filename" == "README.md" || "$filename" == "CHANGELOG.md" ]] && continue

        local content
        content=$(cat "$filepath")

        # Parse frontmatter
        local fm
        fm=$(extract_frontmatter "$content")

        local concept_type=$(echo "$fm" | awk '/^type:/ {sub(/^type: /, ""); gsub(/^[" ]+|[" ]+$/, ""); print; exit}')
        [[ -z "$concept_type" ]] && continue

        concepts_checked=$((concepts_checked + 1))

        # Get latest verification timestamp
        local verified_at
        verified_at=$(extract_latest_verified "$content")
        if [[ -z "$verified_at" ]]; then
            verified_at=$(extract_generated_at "$content")
        fi
        [[ -z "$verified_at" ]] && continue

        local verified_epoch
        verified_epoch=$(parse_iso_to_epoch "$verified_at")
        [[ "$verified_epoch" == "0" ]] && continue

        # Extract subtype_of versions
        local subtypes
        subtypes=$(extract_subtype_versions "$content")

        while IFS='=' read -r abstract_type abstract_version; do
            [[ -z "$abstract_type" || -z "$abstract_version" ]] && continue

            # Only check base version entities
            [[ "$abstract_version" != "v0.1.0" ]] && continue

            local changed
            changed=$(check_abstract_changed "$abstract_type" "$abstract_version" "$verified_epoch" "$ABSTRACTS_REPO")

            if [[ "$changed" == "changed" ]]; then
                local rel_path=$(realpath --relative-to="$BUNDLE_PATH" "$filepath" 2>/dev/null || basename "$filepath")
                echo -e "${YELLOW}[WARN]${NC} $rel_path: $abstract_type ($abstract_version) may have changed since verification ($(date -d "@$verified_epoch" "+%Y-%m-%d" 2>/dev/null || date -r "$verified_epoch" "+%Y-%m-%d" 2>/dev/null))"
                warnings=$((warnings + 1))
            fi
        done <<< "$subtypes"
    done

    log_info "Checked $concepts_checked concepts"

    if [[ $warnings -gt 0 ]]; then
        return 1
    fi
    return 0
}

# Main
main() {
    log_info "Checking abstract lineage for bundle: $BUNDLE_PATH"
    [[ -n "$ABSTRACTS_REPO" ]] && log_info "Using abstracts repo: $ABSTRACTS_REPO"

    local exit_code=0
    check_bundle "$BUNDLE_PATH" "$ABSTRACTS_REPO" || exit_code=1

    if [[ $exit_code -eq 0 ]]; then
        log_info "All concepts up-to-date with abstract versions"
    else
        log_warn "Some concepts may need re-verification"
    fi

    exit $exit_code
}

main "$@"
