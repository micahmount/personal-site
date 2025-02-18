import os
import re
import shutil

# Paths
posts_dir = "/home/micah/Sites/micahmount.com/content/blog/"
attachments_dir = "/home/micah/Documents/notes/Obsidian Vault - personal/attachments/"
static_images_dir = "/home/micah/Sites/micahmount.com/static/img/"

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
