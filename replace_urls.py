import os
import glob

html_dir = os.path.join(os.path.dirname(__file__), "Projest")
html_files = glob.glob(os.path.join(html_dir, "*.html"))

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We want to replace 'http://127.0.0.1:8000/api/...' with `${window.location.protocol}//${window.location.hostname}:8000/api/...`
    # Also handle backticks and double quotes if any.
    
    # First, handle single quotes: 'http://127.0.0.1:8000
    content = content.replace("'http://127.0.0.1:8000", "`\\${window.location.protocol}//\\${window.location.hostname}:8000")
    
    # Next, handle double quotes: "http://127.0.0.1:8000
    content = content.replace('"http://127.0.0.1:8000', "`\\${window.location.protocol}//\\${window.location.hostname}:8000")
    
    # Next, handle backticks: `http://127.0.0.1:8000
    content = content.replace("`http://127.0.0.1:8000", "`\\${window.location.protocol}//\\${window.location.hostname}:8000")
    
    # Finally, if there is a raw http://127.0.0.1:8000 that wasn't caught (e.g. inside a backtick already)
    # Actually if it was inside a backtick it would just be `http://127.0.0.1...`
    # Let's just do a plain string replace for any leftovers (but carefully).
    content = content.replace("http://127.0.0.1:8000", "${window.location.protocol}//${window.location.hostname}:8000")
    
    # Wait, the single quote replacement changed 'http://127.0.0.1:8000/api/me' to `${window.location.protocol}...`
    # Note that the string now ends with a single quote: `${...}/api/me'
    # We must also replace the closing single quote with a backtick!
    # Instead of doing that, it's easier to just do:
    # content.replace("'http://127.0.0.1:8000", "`http://127.0.0.1:8000") 
    # to standardize, then replace ending single quote? No, that's brittle.
    pass

# Better approach using regex
import re

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find: 'http://127.0.0.1:8000/api/something'
    # Replace with: `${window.location.protocol}//${window.location.hostname}:8000/api/something`
    
    # Match 'http://127.0.0.1:8000/...' or "http://127.0.0.1:8000/..."
    def repl_func(match):
        url_path = match.group(1)
        return f"`${{window.location.protocol}}//${{window.location.hostname}}:8000{url_path}`"
        
    content = re.sub(r"['\"]http://127\.0\.0\.1:8000([^'\"]*)['\"]", repl_func, content)
    
    # Also handle backticks: `http://127.0.0.1:8000/api/${userId}`
    def repl_func_bt(match):
        url_path = match.group(1)
        return f"`${{window.location.protocol}}//${{window.location.hostname}}:8000{url_path}`"
        
    content = re.sub(r"`http://127\.0\.0\.1:8000([^`]*)`", repl_func_bt, content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Replacement complete.")
