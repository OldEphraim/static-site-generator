import os
import shutil
from utils import generate_pages_recursive

def main():
    # Delete anything in the public directory
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public", exist_ok=True)

    # Copy static files from static to public
    shutil.copytree("static", "public/static", dirs_exist_ok=True)

    # Generate the page from content/index.md using template.html
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()