from flask import Flask, request, jsonify

app = Flask(__name__)

def predict_academic_result(input_data):
    # Input values
    internet = input_data.get("Internet_Access_at_Home", "No")
    parent_edu = input_data.get("Parent_Education_Level", "None")
    stress = input_data.get("Stress_Level", 3)
    sleep_hours = input_data.get("Sleep_Hours_per_Night_Entier", 7)

    # Step 1: Estimate probability of passing (dummy logic)
    prob = 0.3  # base probability
    if internet == "Yes":
        prob += 0.15
    if parent_edu == "College":
        prob += 0.15
    if stress <= 2:
        prob += 0.15
    if 7 <= sleep_hours <= 9:
        prob += 0.1

    prob = max(0.0, min(1.0, prob))  # clamp between 0 and 1

    # Step 2: Assign grade based on probability
    if prob >= 0.85:
        grade = "A"
    elif prob >= 0.70:
        grade = "B"
    elif prob >= 0.50:
        grade = "C"
    elif prob >= 0.40:
        grade = "D"
    else:
        grade = "F"

    # Step 3: Assign pass/fail based on grade
    if grade in ["A", "B", "C", "D"]:
        result = "Passed"
    else:
        result = "Failed"

    # Step 4: Sleep recommendation
    if sleep_hours < 7:
        sleep_note = "Try to get more sleep (7–9 hours is recommended)."
    elif sleep_hours > 9:
        sleep_note = "You're sleeping more than the recommended range (7–9 hours)."
    else:
        sleep_note = "Your sleep is within the recommended range (7–9 hours)."

    return {
        "Estimated_Grade": grade,
        "Probability_Passed": round(prob, 3),
        "Recommended_Sleep_Hours": sleep_note,
        "Result": result
    }


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    try:
        prediction = predict_academic_result(data)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
