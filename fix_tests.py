import os

def replace_in_dir(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                new_content = content.replace("s.scheme_id", "s.id")
                new_content = new_content.replace("scheme_name", "name")
                
                # Fix test_eligibility.py specific assertions
                new_content = new_content.replace('assert "min_age" in res["failed_conditions"]', 'assert any("age requirement" in cond for cond in res["failed_conditions"])')
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Updated {filepath}")

replace_in_dir("backend/tests")
replace_in_dir("backend/services")
replace_in_dir("backend/rag")
replace_in_dir("backend/api")
replace_in_dir("backend/conversation")
replace_in_dir("tests")
