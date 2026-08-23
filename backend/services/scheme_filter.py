from typing import List
from backend.models.citizen import CitizenProfile
from backend.models.scheme import Scheme

def filter_schemes(schemes: List[Scheme], citizen: CitizenProfile) -> List[Scheme]:
    filtered = []
    
    for scheme in schemes:
        # Step 1: Remove inactive schemes
        if scheme.status.lower() != "active":
            continue
            
        keep = True
        
        # Step 2: Check State
        allowed_states = scheme.eligibility.states or []
        if scheme.state and scheme.state != "All":
            allowed_states.append(scheme.state)
            
        if citizen.state and allowed_states and "All" not in allowed_states:
            if citizen.state not in allowed_states:
                keep = False
                
        # Step 3: Check Beneficiary relevance
        if scheme.target_beneficiaries:
            targets = [t.lower() for t in scheme.target_beneficiaries]
            is_female_specific = any(t in ["female", "pregnancy", "maternity", "girl_child"] for t in targets)
            
            # If the scheme is exclusively female-specific (no 'all', 'male', etc.)
            if is_female_specific and "all" not in targets and "male" not in targets:
                # If gender is known to be Male
                if citizen.gender and citizen.gender.lower() == "male":
                    # And beneficiary is Self
                    if citizen.beneficiary_for and citizen.beneficiary_for.lower() == "self":
                        keep = False
                        
        # Step 4: Check Occupation (user-type relevance)
        if citizen.occupation and scheme.eligibility.occupations:
            if citizen.occupation not in scheme.eligibility.occupations:
                keep = False
                
        # Check Category
        if citizen.category and scheme.eligibility.categories:
            if citizen.category not in scheme.eligibility.categories:
                keep = False
                
        if keep:
            filtered.append(scheme)
            
    return filtered
