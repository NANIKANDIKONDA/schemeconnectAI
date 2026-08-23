from backend.llm.gemini_client import generate_text
import json

def generate_clarification_request(missing_fields: list, intent: str) -> str:
    """Ask user for missing fields without interrogating."""
    intent_desc = intent.replace("_", " ") if intent else "relevant"
    prompt = f"""
    The user is looking for {intent_desc} schemes. We need more information to accurately determine eligibility.
    Please ask the user politely and concisely to provide the following missing details: {', '.join(missing_fields)}.
    Do not interrogate them. Be friendly and helpful.
    """
    response = generate_text(prompt)
    if response:
        return response
    
    # Fallback
    friendly_fields = ", ".join([f.replace("_", " ") for f in missing_fields])
    return f"To check eligibility more accurately for {intent_desc} schemes, please provide your: {friendly_fields}."

def generate_final_response(citizen_dict: dict, ranked_schemes: list) -> str:
    """Generate final response based on backend output."""
    if not ranked_schemes:
        return "I could not find any relevant schemes based on your current profile."
        
    # Build payload for LLM
    top_results = []
    for item in ranked_schemes[:3]: # top 3
        s = item["scheme"]
        r = item["result"]
        top_results.append({
            "scheme_name": s.name,
            "category": s.category,
            "status": r["eligibility_status"],
            "matched_conditions": len(r["matched_conditions"]),
            "official_source": s.official_link
        })
        
    payload = {
        "citizen": citizen_dict,
        "top_results": top_results
    }
    
    prompt = f"""
    You are an AI assistant for SchemeConnect AI.
    Based on the verified backend results, generate a helpful response to the user.
    Do NOT invent any schemes, benefits, or criteria. Use ONLY the data provided.
    
    Backend Data:
    {json.dumps(payload, indent=2)}
    
    For each scheme, state the eligibility status, briefly explain why based on their profile, and ALWAYS include the Official Source link if available.
    If no URL is available, say: "Official application link is not currently available in our verified dataset."
    Remind the user to verify requirements on the official site.
    Format your response clearly.
    """
    
    response = generate_text(prompt)
    if response:
        return response
        
    # Fallback without Gemini
    text = "Based on your information, here are the most relevant schemes:\n\n"
    for r in top_results:
        text += f"{r['scheme_name']}\nStatus: {r['status']}\n"
        if r['official_source']:
            text += f"Official Source: {r['official_source']}\n\n"
        else:
            text += "Official application link is not currently available in our verified dataset.\n\n"
    text += "Please verify the final application requirements through the official government source before applying."
    return text
