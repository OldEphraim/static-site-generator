# utils.py
import os
import markdown
import re

def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()  # Remove the '# ' and strip whitespace
    raise Exception("No H1 header found in the markdown")

def markdown_to_html_code(markdown_content: str) -> str:
    """Convert Markdown content to HTML."""
    html = markdown.markdown(markdown_content)

    # Post-process to replace <em> with <i>
    html = html.replace('<em>', '<i>').replace('</em>', '</i>')
    html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')

    # Regular expression to match <blockquote><p>...</p></blockquote> and convert to <blockquote>...</blockquote>
    html = re.sub(r'<blockquote>\s*<p>(.*?)</p>\s*</blockquote>', r'<blockquote>\1</blockquote>', html, flags=re.DOTALL)

    return html

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown_to_html_code(markdown_content)
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the full HTML page to the destination path
    with open(dest_path, 'w') as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    """Crawl the content directory and generate HTML pages from markdown files."""
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                markdown_path = os.path.join(root, file)
                
                # Generate the corresponding HTML path
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                html_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + '.html')

                # Generate the page
                generate_page(markdown_path, template_path, html_path)

