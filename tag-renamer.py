import os
import frontmatter

def process_markdown_files(directory):
    """Recursively processes all markdown files, ignoring '_index.md'."""
    ignored_tags = []
    with open('tags-ignorelist.txt', "r", encoding="utf-8") as f:
        ignored_tags = f.read().splitlines()

    print(f"Ignored tags: {ignored_tags}")

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and file != "_index.md":  # Ignore _index.md
                filepath = os.path.join(root, file)

                # Load markdown file
                with open(filepath, "r", encoding="utf-8") as f:
                    post = frontmatter.loads(f.read())

                # Ensure taxonomies and tags keys exist
                if 'taxonomies' not in post.metadata:
                    post.metadata['taxonomies'] = {}
                if 'tags' not in post.metadata['taxonomies']:
                    post.metadata['taxonomies']['tags'] = []

                # Update front matter with generated tags
                for index, tag in enumerate(post.metadata['taxonomies']['tags']):
                    if isinstance(tag, str) and '-' in tag and tag not in ignored_tags:
                        post.metadata['taxonomies']['tags'][index] = tag.replace('-', ' ')

                print(f"Tags: {post.metadata['taxonomies']['tags']}")

                # Save the modified file
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))

                print(f"Updated: {filepath}")

# Define the root directory where Markdown files are stored
process_markdown_files(os.getenv("MARKDOWN_DIR"))
