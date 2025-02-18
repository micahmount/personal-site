---
title: Automating My Blog with Obsidian and Hugo
date: 2024-12-18T23:17:04-08:00
description: Resurrecting my blog using Obsidian
tags:
  - blog
  - software
  - obsidian
  - hugo
categories:
  - tools
  - getting started
draft: false
---
# Automating My Blog with Obsidian and Hugo

I've been meaning to resurrect my blog for months; but it just never seemed _quite_ important enough; then inspiration struck when Network Chuck did a great video & post about doing exactly what I had been planning; use Obsidian as a second brain[^1] and writing tool; then sync blog posts to Hugo. Here are his [video](https://www.youtube.com/watch?v=dnE7c0ELEH8&t=1198s) and [blog post](https://blog.networkchuck.com/posts/my-insane-blog-pipeline/); check them out--they're great!

While Chuck achieved exactly what I had planned on doing, I wanted a little different workflow. He automated everything from Obsidian to publishing in one go; whereas I wanted to break that up a bit. I want to automate syncing what I write in Obsidian over to Hugo so that my blog posts are ready to go, but I prefer to publish in a separate step. So I set about building on top of what Chuck had already done, and modified it to fit my preferences.

To accomplish this I need to do 2 things:
1. Copy blog posts from Obsidian to Hugo.
2. Find any attachments referenced in any of the copied blog posts, move those to Hugo, and update the link(s) in the blog posts.

## Step 1: Copy blog posts from Obsidian to Hugo

There are lots of ways to accomplish this; I want something easy, idempotent, and lightweight so that it can live in my blog repo and I won't lose it. So I wrote a bash script (actually I borrowed _heavily_ from Chuck--thanks Chuck!) that uses rsync to sync the two directories:

```bash
#!/bin/bash
set -euo pipefail

# Change to the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"


# Set variables for Obsidian to Hugo copy
ObsidianPostsPath="/path/to/obsidian/blog/"
HugoPostsPath="/path/to/hugo/blog/"

# Step 1: Sync blog posts from the Obsidian blog vault to the Hugo blog directory; creating new posts, updating old posts, and leaving content that's newer in the Hugo directory untouched.

echo "Syncing posts from Obsidian..."
rsync -avz --delete "$ObsidianPostsPath" "$HugoPostsPath"
```

## Step 2: Handle links to local resources

This step is interesting because there are actually a few different needs:
- Find all of the links in blog posts that haven't been updated yet.
- Copy link sources from Obsidian to Hugo.
- Update the blog posts with the new link.

In my case these "local resources" are images that I've pasted into a post, so while they don't _have_ to be images, I'll refer to them as images from here on out, and that's also what I'm going to call my Python script--again, borrowing heavily from Network Chuck here--it really _is_ amazing how closely his project matches my preconceived requirements--score!

images.py
```python:images.py

import os
import re
import shutil

# Paths
posts_dir = "/path/to/hugo/blog/"
attachments_dir = "/path/to/obsidian/attachments/"
static_images_dir = "/path/to/hugo/attachments/"

# Step 1: Process each markdown file in the Hugo posts directory (posts_dir), 
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r") as file:
            content = file.read()
        
        # Step 2: Find all .png image links in the format '[]*.png'.
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces, and prepending the '/img/' dir.
            markdown_image = f"[Image Description](/img/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Step 4: Copy the image to the Hugo static/images directory if it exists
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")

```


## Wrapping up

To make life easier, I added running the python script into the bash scrip so that with one command my blog would be fully updated and ready for QA; here's that second part:

```bash
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

```


The entire script looks like this:
```bash
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

```


From here I just made sure that both the `images.py` & `import_posts.sh` files were in the root directory of my blog, and that the bash script was executable by running `chmod +x import_posts.sh` on the command line while in the same directory.

And with that my I can now enjoy creating content in Obsidian, and easily publish it with Hugo just by going to my Hugo directory and running `import_posts.sh` **Boom!**


[^1]: If you're not familiar with this term, see the excellent book ["Building a Second Brain" by Tiago Forte](https://a.co/d/8Q3BUla)

