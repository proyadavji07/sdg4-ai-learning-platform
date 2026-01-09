def analyze_learning_gap(score, total_questions):
    accuracy = (score / total_questions) * 100

    if accuracy < 60:
        status = "Weak"
    elif accuracy < 80:
        status = "Moderate"
    else:
        status = "Strong"

    return accuracy, status
