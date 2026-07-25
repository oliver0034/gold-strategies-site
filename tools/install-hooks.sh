#!/bin/sh
#
# install-hooks.sh — installe le garde-fou pre-push dans ce clone du dépôt.
#
# Les hooks git ne sont pas versionnés : à relancer après un nouveau clone.
#   sh tools/install-hooks.sh

set -e
repo_root=$(git rev-parse --show-toplevel)
hooks_dir="$repo_root/.git/hooks"

mkdir -p "$hooks_dir"
cp "$repo_root/tools/pre-push" "$hooks_dir/pre-push"
chmod +x "$hooks_dir/pre-push"

echo "✓ hook pre-push installé dans .git/hooks/"
echo "  Il lance tools/check-site.py avant chaque push et bloque si le site partirait cassé."
