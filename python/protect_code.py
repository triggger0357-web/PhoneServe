import os

# Your Proprietary Legal Notice
LEGAL_NOTICE = """/* * PROPERTY OF DAVID INGALLS | EDGE TECH (EDGE TECH KNOWLEDGEY)
 * COPYRIGHT © 2026. ALL RIGHTS RESERVED.
 * * STRICTLY PROHIBITED: UNAUTHORIZED COMMERCIAL USE, MONETIZATION, 
 * OR DISTRIBUTION WITHOUT WRITTEN CONSENT AND COMPENSATION.
 * * CONTACT: triggger0357@gmail.com | 503-990-4004 (TEXT ONLY)
 */

"""

def add_header_to_files():
    # List the file types you want to protect (e.g., .py, .js, .cpp)
    extensions = ('.py', '.js', '.cpp', '.h', '.css')
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(extensions) and file != "protect_code.py":
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check if the notice is already there to avoid duplicates
                if "PROPERTY OF DAVID INGALLS" not in content:
                    print(f"Protecting: {file}")
                    with open(file_path, 'w') as f:
                        f.write(LEGAL_NOTICE + content)

if __name__ == "__main__":
    add_header_to_files()
    print("\n[SUCCESS] All files updated with proprietary protection.")
