#!/usr/bin/env bash
# generate-bdd-synth.sh: The meta-template that turns a single user-requirement
# into a runnable Cucumber/Playwright test skeleton.
#
# Usage (run from within this skill folder):
#   bash generate-bdd-synth.sh <requirements.txt> <output_dir>
#
# The script does NOT execute tests — it emits files into <output_dir>.

set -euo pipefail

REQUIREMENTS="${1:-}"
OUT_DIR="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- sanity checks ---
if [[ -z "$REQUIREMENTS" || -z "$OUT_DIR" ]]; then
  echo "Usage: bash generate-bdd-synth.sh <requirements.txt> <output_dir>"
  exit 1
fi

if [[ ! -f "$REQUIREMENTS" ]]; then
  echo "Error: requirements file not found: $REQUIREMENTS"
  exit 1
fi

mkdir -p "$OUT_DIR"

# --- emit boilerplate (copied once per project) ---
cp "$SCRIPT_DIR/templates/tsconfig.json"    "$OUT_DIR/tsconfig.json"
cp "$SCRIPT_DIR/templates/cucumber.js"       "$OUT_DIR/cucumber.js"
cp "$SCRIPT_DIR/templates/package.json"      "$OUT_DIR/package.json"
cp "$SCRIPT_DIR/templates/.env.example"      "$OUT_DIR/.env.example"
cp "$SCRIPT_DIR/templates/world.ts"         "$OUT_DIR/world.ts"

mkdir -p "$OUT_DIR/features"

# --- transform each line of requirements.txt into a feature + steps ---
line_no=0
while IFS= read -r raw_line; do
  line_no=$((line_no + 1))
  line="$(echo "$raw_line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

  # skip empty lines / comments
  [[ -z "$line" || "$line" == \#* ]] && continue

  # slugify for filenames
  slug="$(echo "$line" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
  featureFile="$OUT_DIR/features/${slug}.feature"
  stepsFile="$OUT_DIR/features/${slug}.steps.ts"

  # --- generate .feature ---
  cat > "$featureFile" <<FEATURE
Feature: $(echo "$line" | sed -E 's/^(User can |User sees |User | user can | user sees | user )//i')
  As a user
  I want to $(echo "$line" | sed -E 's/^(User can |User sees |User | user can | user sees | user )//i')
  So that the application behaves correctly

  Scenario: ${line}
    Given the user is on the relevant page
    When the user performs the action for "${line}"
    Then the expected outcome for "${line}" is displayed
FEATURE

  # --- generate .steps.ts ---
  # We keep the same placeholder structure contained in the official skill template.
  cat > "$stepsFile" <<STEPS
import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { ICustomWorld } from '../world';

Given('the user is on the relevant page', async function (this: ICustomWorld) {
  await this.page!.goto(process.env.BASE_URL!);
});

When('the user performs the action for "${line}"', async function (this: ICustomWorld) {
  // TODO: implement Playwright action (click, fill, etc.)
});

Then('the expected outcome for "${line}" is displayed', async function (this: ICustomWorld) {
  // TODO: implement assertion with Playwright
});
STEPS

done < "$REQUIREMENTS"

echo "✅ Generated BDD test suite in $OUT_DIR"
echo "   Features : $OUT_DIR/features/"
echo "   Next step: cd $OUT_DIR && npm install && npx playwright install && npm test"
