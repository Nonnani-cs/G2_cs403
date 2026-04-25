import sys

def check_html(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    stack = []
    # Very simple tag checker
    import re
    tags = re.findall(r'<(/?)([a-z1-6]+)', content.lower())
    
    ignore_tags = ['meta', 'link', 'br', 'hr', 'img', 'input', 'source']
    
    for closing, tag in tags:
        if tag in ignore_tags:
            continue
        if closing:
            if not stack:
                print(f"Error: Unexpected closing tag </{tag}>")
            else:
                last_tag = stack.pop()
                if last_tag != tag:
                    print(f"Error: Mismatched tag </{tag}>, expected </{last_tag}>")
        else:
            stack.append(tag)
    
    if stack:
        print(f"Error: Unclosed tags: {stack}")
    else:
        print("No mismatched tags found (simple check).")

print("Checking receive.html:")
check_html('/Users/atcharapornn/Desktop/Projest/receive.html')
print("\nChecking manage.html:")
check_html('/Users/atcharapornn/Desktop/Projest/manage.html')
