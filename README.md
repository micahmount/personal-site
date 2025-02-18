# <https://micahmount.com> - A Hugo site

## Purpose

I wanted a personal website; somewhere to showcase my personal projects, as well as a blog where I could publish all the fun little projects I putter around with.

## 🛠️ Development

The site is built with [Hugo](https://gohugo.io), the [Quick start guide](https://gohugo.io/getting-started/quick-start/) stays up to date, but in general once Hugo is installed (see below), simply run `hugo server` in the root directory to compile and start.

### 🚧 Requirements

Hugo only requires git and [Hugo](https://gohugo.io/installation/) to get up and running.

## 🚀 Blog Automation

 I added a set of tools to automate syncing blog posts between Obsidian and Hugo. This automation handles both content synchronization and image management.

## Overview

This toolset provides two main functions:

1. Syncs blog posts from Obsidian to Hugo using rsync
2. Processes image attachments:
   - Finds image references in blog posts
   - Copies images from Obsidian attachments to Hugo static directory
   - Updates image links in blog posts to use Hugo's format

## Prerequisites

- Python 3.x
- rsync
- Bash shell
- Obsidian vault with blog posts
- Hugo blog setup

## Setup

1. Clone this repository to your local machine
2. Update the paths in both `images.py` and `import_posts.sh`:

In `images.py`:
    ```python
    posts_dir = "/path/to/hugo/blog/"               # Your Hugo blog posts directory
    attachments_dir = "/path/to/obsidian/attachments/" # Your Obsidian attachments directory
    static_images_dir = "/path/to/hugo/static/img/"    # Your Hugo static images directory
    ```

In `import_posts.sh`:
    ```bash
    ObsidianPostsPath="/path/to/obsidian/blog/"    # Your Obsidian blog posts directory
    HugoPostsPath="/path/to/hugo/blog/"            # Your Hugo blog posts directory
    ```

## Usage

Run the import script from the terminal:

```bash
./import_posts.sh
```

This will:

1. Sync all blog posts from Obsidian to Hugo
2. Process any image links in the posts
3. Copy referenced images to Hugo's static directory

## File Structure

- `import_posts.sh` - Main bash script that orchestrates the sync process
- `images.py` - Python script that handles image processing and link updates

## Image Formatting

The script looks for Obsidian-style image links (`[[image.png]]`) and converts them to Hugo-compatible Markdown links (`[Image Description](/img/image.png)`).

## Notes

- The sync is one-way (Obsidian → Hugo)
- The script uses `rsync` with the `--delete` flag, so files removed from Obsidian will also be removed from Hugo
- Make sure to backup your Hugo blog content before first use

## Credits

Based on Network Chuck's blog automation system, modified to separate the sync and publish steps.
