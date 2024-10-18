from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect the form data
    feature_name = request.form['feature_name']
    persona = request.form['persona']
    
    # Simulate predictions (use your machine learning model here)
    adoption = 85.0  # Example prediction for feature adoption likelihood
    engagement = 9  # Example engagement level out of 10
    pain_points = 3  # Example pain points prediction out of 10

    # Render result.html with the prediction results
    return render_template('result.html', feature_name=feature_name, persona=persona, 
                           adoption=adoption, engagement=engagement, pain_points=pain_points)

if __name__ == '__main__':
    app.run(debug=True)
