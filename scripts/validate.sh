#!/bin/bash
# Validate marketplace.json against schema

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
MARKETPLACE_FILE="$REPO_ROOT/.claude-plugin/marketplace.json"
SCHEMA_FILE="$REPO_ROOT/schema/marketplace-schema.json"

echo "Validating marketplace.json..."

# Check if files exist
if [ ! -f "$MARKETPLACE_FILE" ]; then
    echo "Error: marketplace.json not found at $MARKETPLACE_FILE"
    exit 1
fi

if [ ! -f "$SCHEMA_FILE" ]; then
    echo "Error: schema file not found at $SCHEMA_FILE"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it to validate JSON."
    echo "  macOS: brew install jq"
    echo "  Linux: sudo apt-get install jq"
    exit 1
fi

# Validate JSON syntax
if jq empty "$MARKETPLACE_FILE" 2>/dev/null; then
    echo "✓ JSON syntax is valid"
else
    echo "✗ Invalid JSON syntax in marketplace.json"
    exit 1
fi

# Check required fields
NAME=$(jq -r '.name // empty' "$MARKETPLACE_FILE")
OWNER=$(jq -r '.owner.name // empty' "$MARKETPLACE_FILE")
PLUGINS=$(jq -r '.plugins // empty' "$MARKETPLACE_FILE")

if [ -z "$NAME" ]; then
    echo "✗ Missing required field: name"
    exit 1
fi
echo "✓ Marketplace name: $NAME"

if [ -z "$OWNER" ]; then
    echo "✗ Missing required field: owner.name"
    exit 1
fi
echo "✓ Owner: $OWNER"

if [ "$PLUGINS" = "" ]; then
    echo "✗ Missing required field: plugins"
    exit 1
fi

PLUGIN_COUNT=$(jq '.plugins | length' "$MARKETPLACE_FILE")
echo "✓ Plugin count: $PLUGIN_COUNT"

# Validate each plugin entry
echo ""
echo "Validating plugin entries..."

if [ "$PLUGIN_COUNT" -gt 0 ]; then
    for i in $(seq 0 $((PLUGIN_COUNT - 1))); do
        PLUGIN_NAME=$(jq -r ".plugins[$i].name // empty" "$MARKETPLACE_FILE")
        PLUGIN_SOURCE=$(jq -r ".plugins[$i].source // empty" "$MARKETPLACE_FILE")

        if [ -z "$PLUGIN_NAME" ]; then
            echo "✗ Plugin $i: Missing name"
            exit 1
        fi

        if [ -z "$PLUGIN_SOURCE" ]; then
            echo "✗ Plugin $i ($PLUGIN_NAME): Missing source"
            exit 1
        fi

        echo "✓ Plugin $i: $PLUGIN_NAME"
    done
else
    echo "(No plugins to validate)"
fi

echo ""
echo "✓ Marketplace validation passed!"
