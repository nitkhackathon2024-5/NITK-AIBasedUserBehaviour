

from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained models
with open('models/smart_assistant_adoption_model.pkl', 'rb') as f:
    smart_assistant_adoption_model = pickle.load(f)

with open('models/smart_assistant_engagement_model.pkl', 'rb') as f:
    smart_assistant_engagement_model = pickle.load(f)

with open('models/card_management_adoption_model.pkl', 'rb') as f:
    card_management_adoption_model = pickle.load(f)

with open('models/card_management_engagement_model.pkl', 'rb') as f:
    card_management_engagement_model = pickle.load(f)

with open('models/investment_tools_adoption_model.pkl', 'rb') as f:
    investment_tools_adoption_model = pickle.load(f)

with open('models/investment_tools_engagement_model.pkl', 'rb') as f:
    investment_tools_engagement_model = pickle.load(f)

with open('models/mobile_banking_adoption_model.pkl', 'rb') as f:
    mobile_banking_adoption_model = pickle.load(f)

with open('models/mobile_banking_engagement_model.pkl', 'rb') as f:
    mobile_banking_engagement_model = pickle.load(f)

# Encode persona into numerical values
persona_encoding = {
    "Tech-Savvy Millennial": 0,
    "Busy Professional": 1,
    "Small Business Owner": 2,
    "Retiree/Conservative Investor": 3,
    "Frequent Traveler/Expat": 4,
    "New-to-Banking/Rural User": 5,
    "High-Net-Worth Individual (HNI)": 6
}

# Default features to fill the remaining feature space
DEFAULT_FEATURES = [0] * 14

def predict_adoption(model, input_data):
    return model.predict_proba(input_data)[0][1] * 100

def predict_engagement(model, input_data):
    return model.predict(input_data)[0]

def get_pain_points(feature, persona):
    # Hard-coded pain points based on the selected feature and persona
    pain_points = {
        "smart_assistant": {
            "Tech-Savvy Millennial": "Privacy concerns, Integration issues with other devices",
            "Busy Professional": "Difficulty in customization, Limited functionality in specific use cases",
            "Small Business Owner": "Cost of deployment, Training employees on usage",
            "Retiree/Conservative Investor": "Complex user interface, Trust in AI decision-making",
            "Frequent Traveler/Expat": "Connectivity issues, Language support limitations",
            "New-to-Banking/Rural User": "Difficulty in understanding technology, Initial setup challenges",
            "High-Net-Worth Individual (HNI)": "Concerns about data security, Preference for human advisors"
        },
        "card_management": {
            "Tech-Savvy Millennial": "Limited app functionality, Lack of real-time notifications",
            "Busy Professional": "User interface complexity, Time-consuming card setup process",
            "Small Business Owner": "Inflexibility in payment options, Transaction limits",
            "Retiree/Conservative Investor": "Difficulty in navigating digital interfaces, Lack of customer support",
            "Frequent Traveler/Expat": "International transaction fees, Card compatibility issues",
            "New-to-Banking/Rural User": "Unfamiliarity with digital payments, Difficulty in understanding card features",
            "High-Net-Worth Individual (HNI)": "Limited personalization options, Premium services not being well-defined"
        },
        "investment_tools": {
            "Tech-Savvy Millennial": "Limited investment options, Lack of educational resources",
            "Busy Professional": "Complicated interface, Insufficient time to track investments",
            "Small Business Owner": "Inadequate support for business-specific needs, Lack of automation",
            "Retiree/Conservative Investor": "Preference for traditional methods, Risk of new technology",
            "Frequent Traveler/Expat": "Currency conversion issues, Tax implications",
            "New-to-Banking/Rural User": "Unfamiliarity with investment terms, Difficulty in understanding returns",
            "High-Net-Worth Individual (HNI)": "Concerns over advisory fees, Desire for more sophisticated tools"
        },
        "mobile_banking": {
            "Tech-Savvy Millennial": "App crashes, Limited features compared to web",
            "Busy Professional": "Slow customer service, App security concerns",
            "Small Business Owner": "Limited integration with accounting software, Transaction limits",
            "Retiree/Conservative Investor": "Preference for in-person banking, Difficulty in navigating the app",
            "Frequent Traveler/Expat": "Location-specific restrictions, Poor connectivity in certain regions",
            "New-to-Banking/Rural User": "Low digital literacy, Difficulty in setting up online banking",
            "High-Net-Worth Individual (HNI)": "Concerns over data breaches, Limited concierge services"
        }
    }

    # Retrieve the pain points for the selected feature and persona, default to "No specific pain points found" if not available
    return pain_points.get(feature, {}).get(persona, "No specific pain points found")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input values from the form
        age = float(request.form['age'])
        tech_savviness = float(request.form['tech_savviness'])
        income = float(request.form['income'])
        persona = request.form['persona']
        feature = request.form['feature']

        # Encode the persona
        persona_encoded = persona_encoding.get(persona, -1)

        # Combine user inputs with default values to match the expected shape of 18 features
        user_features = [age, tech_savviness, income, persona_encoded]
        input_data = np.array([user_features + DEFAULT_FEATURES])

        # Select the appropriate models based on the selected feature
        if feature == "smart_assistant":
            adoption_prob = predict_adoption(smart_assistant_adoption_model, input_data)
            expected_engagement = predict_engagement(smart_assistant_engagement_model, input_data)
        elif feature == "card_management":
            adoption_prob = predict_adoption(card_management_adoption_model, input_data)
            expected_engagement = predict_engagement(card_management_engagement_model, input_data)
        elif feature == "investment_tools":
            adoption_prob = predict_adoption(investment_tools_adoption_model, input_data)
            expected_engagement = predict_engagement(investment_tools_engagement_model, input_data)
        elif feature == "mobile_banking":
            adoption_prob = predict_adoption(mobile_banking_adoption_model, input_data)
            expected_engagement = predict_engagement(mobile_banking_engagement_model, input_data)
        else:
            return jsonify({'error': 'Invalid feature selected'})

        # Get pain points for the selected feature and persona
        pain_points = get_pain_points(feature, persona)

        return render_template(
            'result.html', 
            adoption_probability=round(adoption_prob, 2), 
            expected_engagement=round(expected_engagement, 2),
            persona=persona,
            feature=feature,
            pain_points=pain_points
        )
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
