#!/bin/bash
set -euo pipefail

# Change to the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"


# Set variables for Obsidian to Hugo copy
ObsidianPostsPath="/home/micah/Documents/notes/Obsidian Vault - personal/blog/"
HugoPostsPath="/home/micah/Sites/micahmount.com/content/blog/"

# Step 1: Sync blog posts from the Obsidian blog vault to the Hugo blog directory; creating new posts, updating old posts, and leaving content that's newer in the Hugo directory untouched.

echo "Syncing posts from Obsidian..."
rsync -avz --delete "$ObsidianPostsPath" "$HugoPostsPath"

# Step 2: Process Markdown files with Python script to handle image links
echo "Processing image links in Markdown files..."
if [ ! -f "images.py" ]; then
    echo "Python script images.py not found."
    exit 1
fi

if ! python3 images.py; then
    echo "Failed to process image links."
    exit 1
fi

echo "All done! Blog posts synced, image links updated and images copied over."