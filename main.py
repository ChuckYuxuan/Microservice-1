from flask import Flask, request, jsonify
import openai
import os
from flask import render_template

# Initialize Flask app
app = Flask(__name__)

# Function to query OpenAI API

openai.api_key = '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'
def query_openai(prompt):
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are Professor Donald Ferguson's AI Teaching Assistant."},
                      {"role": "user", "content": prompt}]
        )
        response = completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"
    return response


# Home route
# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle question asking
@app.route('/ask', methods=['POST'])
def ask():
    # Get the question from the POST request
    question = request.json.get('question', '')
    # Get the answer from OpenAI
    answer = query_openai(question)
    # Return the answer as JSON
    return jsonify({"answer": answer})



@app.route('/chat')
def chat():
    return app.send_static_file('index.html')

data_store = {
    1: "Sample question 1",
    2: "Sample question 2",
    3: "Sample question 3",
    4: "Sample question 4",
    5: "Sample question 5",
    6: "Sample question 6",
    7: "Sample question 7",
    8: "Sample question 8",
    9: "Sample question 9",
    10: "Sample question 10",
    11: "Sample question 11",
    12: "Sample question 12",
    13: "Sample question 13",
    14: "Sample question 14",
    15: "Sample question 15",
    16: "Sample question 16",
    17: "Sample question 17",
    18: "Sample question 18",
    19: "Sample question 19",
    20: "Sample question 20"
}


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    if question_id not in data_store:
        return jsonify({"error": "Question not found."}), 404

    question_data = request.json.get('question', '')
    data_store[question_id] = question_data
    return jsonify({"message": "Question updated successfully."})

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    if question_id not in data_store:
        return jsonify({"error": "Question not found."}), 404

    del data_store[question_id]
    return jsonify({"message": "Question deleted successfully."})

@app.route('/questions', methods=['GET'])
def list_questions():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    start = (page - 1) * limit
    end = start + limit
    paginated_data = list(data_store.items())[start:end]
    return jsonify(paginated_data)



# Main execution
if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
