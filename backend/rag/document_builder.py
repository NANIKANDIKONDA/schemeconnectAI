from backend.models.scheme import Scheme

def build_document(scheme: Scheme) -> str:
    """
    Convert a Scheme object into a clean, readable text document.
    """
    elig = scheme.eligibility
    min_age = elig.min_age if elig.min_age is not None else "None"
    max_age = elig.max_age if elig.max_age is not None else "None"
    max_inc = elig.max_income if elig.max_income is not None else "None"
    
    occ = ", ".join(elig.occupations) if elig.occupations else "Any"
    edu = ", ".join(elig.education) if elig.education else "Any"
    cat = ", ".join(elig.categories) if elig.categories else "Any"
    
    min_land = elig.min_land_acres if elig.min_land_acres is not None else "None"
    max_land = elig.max_land_acres if elig.max_land_acres is not None else "None"
    
    states = scheme.state if scheme.state else "All"
    targets = ", ".join(scheme.target_beneficiaries) if scheme.target_beneficiaries else "All"
    benefits = "\n- ".join(scheme.benefits) if scheme.benefits else "None"
    docs = "\n- ".join(scheme.documents_required) if scheme.documents_required else "None"
    
    doc = f"""Scheme Name: {scheme.name}

Category: {scheme.category}

Applicable States: {states}

Target Beneficiaries: {targets}

Description:
{scheme.description}

Eligibility:
Occupation: {occ}
Education: {edu}
Social Category: {cat}
Minimum Age: {min_age}
Maximum Age: {max_age}
Maximum Income: {max_inc}
Land Requirements: Min: {min_land}, Max: {max_land}

Benefits:
- {benefits}

Documents Required:
- {docs}

How to Apply:
{scheme.how_to_apply}

Official Source:
{scheme.official_link}
"""
    return doc
