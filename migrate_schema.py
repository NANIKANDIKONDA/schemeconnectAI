import json

with open("backend/data/schemes.json", "r") as f:
    schemes = json.load(f)

for s in schemes:
    # Rename fields for schema compatibility
    if "scheme_id" in s:
        s["id"] = s.pop("scheme_id")
    if "scheme_name" in s:
        s["name"] = s.pop("scheme_name")
    if "official_source" in s:
        s["official_link"] = s.pop("official_source")
    
    # State handling
    s["state"] = "All"
    if s.get("states"):
        if "All" not in s["states"]:
            s["state"] = s["states"][0]
    
    if "eligibility" in s:
        if "occupation" in s["eligibility"]:
            s["eligibility"]["occupations"] = s["eligibility"].pop("occupation")
        else:
            s["eligibility"]["occupations"] = []
        if "education" not in s["eligibility"]:
            s["eligibility"]["education"] = []
        if "categories" not in s["eligibility"]:
            s["eligibility"]["categories"] = []
        if "genders" not in s["eligibility"]:
            s["eligibility"]["genders"] = []

with open("backend/data/schemes.json", "w") as f:
    json.dump(schemes, f, indent=2)

print("Updated schemes.json")
