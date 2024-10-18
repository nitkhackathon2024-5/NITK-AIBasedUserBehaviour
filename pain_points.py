# pain_points.py

# This dictionary holds potential pain points for each feature and user segment
pain_points_data = {
    "smart_assistant": {
        "low_tech_savviness": "May struggle with voice commands and setup.",
        "high_tech_savviness": "May find the feature too basic, lacking advanced customization options.",
        "low_income": "Might consider the feature a luxury rather than a necessity.",
        "new_to_banking": "May need more guidance on how to use the assistant for banking tasks.",
    },
    "card_management": {
        "low_tech_savviness": "Might find digital card management options confusing.",
        "frequent_traveler": "May experience difficulties with card usage abroad or currency conversion.",
        "low_income": "Concerned about hidden fees or charges related to card services.",
        "retiree": "Prefers face-to-face interactions over digital card management.",
    },
    "investment_tools": {
        "low_tech_savviness": "May find the investment dashboard complex to understand.",
        "high_income": "Might want more detailed analytics and investment tracking.",
        "new_to_banking": "Needs beginner-friendly tutorials to get started with investments.",
        "busy_professional": "Might require automated recommendations due to time constraints.",
    },
    "mobile_banking": {
        "low_tech_savviness": "May find the mobile interface confusing and hard to navigate.",
        "frequent_traveler": "May face issues with international accessibility of mobile banking services.",
        "high_tech_savviness": "Wants more features like cryptocurrency management or API integrations.",
        "small_business_owner": "Might find mobile banking limited for managing business finances.",
    }
}

def get_pain_points(feature, tech_savviness, income, persona):
    """Returns a list of potential pain points based on user attributes."""
    points = []
    
    # General rules for pain points
    if tech_savviness < 3:
        points.append(pain_points_data[feature].get("low_tech_savviness", ""))
    elif tech_savviness > 7:
        points.append(pain_points_data[feature].get("high_tech_savviness", ""))
    
    if income < 30000:
        points.append(pain_points_data[feature].get("low_income", ""))
    elif income > 100000:
        points.append(pain_points_data[feature].get("high_income", ""))
    
    # Persona-specific pain points
    persona_mapping = {
        0: "tech_savvy_millennial",
        1: "busy_professional",
        2: "small_business_owner",
        3: "retiree",
        4: "frequent_traveler",
        5: "new_to_banking",
        6: "high_net_worth_individual"
    }
    
    persona_key = persona_mapping.get(persona)
    if persona_key:
        points.append(pain_points_data[feature].get(persona_key, ""))
    
    # Filter out any empty pain points
    return [point for point in points if point]

