#!/usr/bin/env bash
# generate-bdd-synth.sh: Turn a plain-text requirements file into a runnable
# Cucumber + Playwright + TypeScript BDD test skeleton.
#
# Usage (run from anywhere):
#   bash generate-bdd-synth.sh <requirements.txt> <output_dir>
#
# Layout produced under <output_dir>:
#   <output_dir>/
#   ├── cucumber.js
#   ├── package.json
#   ├── tsconfig.json
#   ├── world.ts
#   ├── .env.example
#   ├── features/<slug>.feature          # Gherkin specs
#   └── steps/<slug>.steps.ts            # Step definitions (Playwright)
#
# The script does NOT execute tests — it only emits files.

set -euo pipefail

REQUIREMENTS="${1:-}"
OUT_DIR="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TPL_DIR="$SCRIPT_DIR/templates"

# --- sanity checks ---
if [[ -z "$REQUIREMENTS" || -z "$OUT_DIR" ]]; then
  echo "Usage: bash generate-bdd-synth.sh <requirements.txt> <output_dir>"
  exit 1
fi

if [[ ! -f "$REQUIREMENTS" ]]; then
  echo "Error: requirements file not found: $REQUIREMENTS"
  exit 1
fi

mkdir -p "$OUT_DIR/features" "$OUT_DIR/steps"

# --- emit project-wide boilerplate (copied once per project) ---
cp "$TPL_DIR/tsconfig.json" "$OUT_DIR/tsconfig.json"
cp "$TPL_DIR/cucumber.js"   "$OUT_DIR/cucumber.js"
cp "$TPL_DIR/package.json"  "$OUT_DIR/package.json"
cp "$TPL_DIR/.env.example"  "$OUT_DIR/.env.example"
cp "$TPL_DIR/world.ts"      "$OUT_DIR/world.ts"

# --- per-line: render .feature and .steps.ts from the templates ---
line_no=0
while IFS= read -r raw_line; do
  line_no=$((line_no + 1))

  # trim leading/trailing whitespace
  line="$(printf '%s' "$raw_line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

  # skip empty lines and comments
  [[ -z "$line" || "$line" == \#* ]] && continue

  # --- derive names from the line ---
  slug="$(printf '%s' "$line" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"

  # Drop a leading "user-can|user-sees|user " so the feature title reads cleanly
  feature_title="$(printf '%s' "$line" \
    | sed -E 's/^(User can |User sees |User | user can | user sees | user )//I')"

  feature_file="$OUT_DIR/features/${slug}.feature"
  steps_file="$OUT_DIR/steps/${slug}.steps.ts"

  # --- render the .feature file from the template ---
  sed \
    -e "s|{{FeatureTitle}}|${feature_title}|g" \
    -e "s|{{FeatureDescription}}|As a user\n  I want to ${feature_title}\n  So that the application behaves correctly|g" \
    -e "s|{{ScenarioDescription}}|${line}|g" \
    -e "s|{{GivenContext}}|the user is on the relevant page|g" \
    -e "s|{{WhenAction}}|the user performs the action for \"${line}\"|g" \
    -e "s|{{ThenOutcome}}|the expected outcome for \"${line}\" is displayed|g" \
    "$TPL_DIR/{{featureName}}.feature" > "$feature_file"

  # --- render the .steps.ts file from the template ---
  # NB: steps live at <root>/steps/<slug>.steps.ts, so the world import is ../../world
  sed \
    -e "s|{{GivenContext}}|the user is on the relevant page|g" \
    -e "s|{{WhenAction}}|the user performs the action for \"${line}\"|g" \
    -e "s|{{ThenOutcome}}|the expected outcome for \"${line}\" is displayed|g" \
    -e "s|import { ICustomWorld } from '../world';|import { ICustomWorld } from '../../world';|" \
    "$TPL_DIR/{{featureName}}.steps.ts" > "$steps_file"
done < "$REQUIREMENTS"

echo "✅ Generated BDD test suite in $OUT_DIR"
echo "   Features : $OUT_DIR/features/"
echo "   Steps    : $OUT_DIR/steps/"
echo "   Next step: cd $OUT_DIR && npm install && npx playwright install && npm test"
