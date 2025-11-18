#!/bin/bash
# Interactive script to add a new plugin to the marketplace

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
MARKETPLACE_FILE="$REPO_ROOT/.claude-plugin/marketplace.json"

echo "======================================"
echo "Add Plugin to Marketplace"
echo "======================================"
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it first."
    echo "  macOS: brew install jq"
    echo "  Linux: sudo apt-get install jq"
    exit 1
fi

# Collect plugin information
read -p "Plugin name (kebab-case): " PLUGIN_NAME
read -p "Description: " DESCRIPTION
read -p "Version (e.g., 1.0.0): " VERSION
read -p "Author: " AUTHOR
read -p "Homepage URL (optional): " HOMEPAGE
read -p "License (e.g., MIT): " LICENSE

echo ""
echo "Source type:"
echo "  1) GitHub repository (owner/repo)"
echo "  2) Git URL (https://...)"
echo "  3) Local path (./plugins/...)"
read -p "Select source type (1-3): " SOURCE_TYPE

case $SOURCE_TYPE in
    1)
        read -p "GitHub repo (owner/repo): " GITHUB_REPO
        SOURCE=$(jq -n --arg repo "$GITHUB_REPO" '{type: "github", repo: $repo}')
        ;;
    2)
        read -p "Git URL: " GIT_URL
        SOURCE=$(jq -n --arg url "$GIT_URL" '{type: "url", url: $url}')
        ;;
    3)
        read -p "Local path: " LOCAL_PATH
        SOURCE="\"$LOCAL_PATH\""
        ;;
    *)
        echo "Invalid source type"
        exit 1
        ;;
esac

# Build plugin entry
PLUGIN_ENTRY=$(jq -n \
    --arg name "$PLUGIN_NAME" \
    --arg desc "$DESCRIPTION" \
    --arg ver "$VERSION" \
    --arg author "$AUTHOR" \
    --arg homepage "$HOMEPAGE" \
    --arg license "$LICENSE" \
    --argjson source "$SOURCE" \
    '{
        name: $name,
        description: $desc,
        version: $ver,
        author: $author,
        source: $source
    } + (if $homepage != "" then {homepage: $homepage} else {} end)
      + (if $license != "" then {license: $license} else {} end)
    ')

echo ""
echo "Plugin entry to add:"
echo "$PLUGIN_ENTRY" | jq .
echo ""

read -p "Add this plugin to marketplace? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "Cancelled"
    exit 0
fi

# Add plugin to marketplace
jq --argjson plugin "$PLUGIN_ENTRY" '.plugins += [$plugin]' "$MARKETPLACE_FILE" > "$MARKETPLACE_FILE.tmp"
mv "$MARKETPLACE_FILE.tmp" "$MARKETPLACE_FILE"

echo ""
echo "✓ Plugin added successfully!"
echo ""
echo "Next steps:"
echo "  1. Run: ./scripts/validate.sh"
echo "  2. Commit the changes"
echo "  3. Push to GitHub"
