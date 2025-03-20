import os
import frontmatter
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tags(content, existing_tags):
    """Uses OpenAI API to generate relevant tags for a given text."""
    response = client.chat.completions.create(model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are an AI that analyzes Markdown content for a Hugo site. Generate single-word, SEO-friendly tags."},
        {"role": "user", "content": f"Without returning any of these tags: \"{existing_tags}\", extract 3 relevant tags from this content and provide them in a simple comma-separated format without any leading numbers:\n\n{content}"}
    ],
    temperature=0.5)
    tags = response.choices[0].message.content
    return [tag.strip().lower().replace('-', ' ') for tag in tags.split(",")]

def process_markdown_files(directory):
    """Recursively processes all markdown files, ignoring '_index.md'."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and file != "_index.md":
                filepath = os.path.join(root, file)

                print(f"Processing: {filepath}")

                # Load markdown file
                with open(filepath, "r", encoding="utf-8") as f:
                    post = frontmatter.loads(f.read())
                    metadata = post.metadata
                    content = post.content

                # Ensure taxonomies and tags keys exist
                if 'taxonomies' not in post.metadata:
                    post.metadata['taxonomies'] = {}
                if 'tags' not in post.metadata['taxonomies']:
                    post.metadata['taxonomies']['tags'] = []

                # remove the 'general' tag if it exists
                if "general" in post.metadata['taxonomies']['tags']:
                    post.metadata['taxonomies']['tags'].remove("general")

                # generate new tags if there are fewer than 3
                tags = []
                if len(metadata['taxonomies']['tags']) < 3:
                    tags = generate_tags(content, metadata['taxonomies']['tags'])

                # Update front matter with generated tags
                for tag in tags:
                    if tag not in post.metadata['taxonomies']['tags']:
                        post.metadata['taxonomies']['tags'].append(tag)

                # Save the modified file
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))

                print(f"Updated: {filepath}")

process_markdown_files(os.getenv("MARKDOWN_DIR"))

print("Auto-tagging completed for all files.")
