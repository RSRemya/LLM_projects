from flask import Flask, render_template, request, redirect, url_for, jsonify
import ollama

app = Flask(__name__)

# Set the model
desiredModel = 'hermes3:8b'

#model_file_path = r"C:\Users\HP\Projects\Flask\Check5\Hermes-3-Llama-3.1-8B.Q4_K_M.gguf"

# Update desiredModel to use the full file path
#desiredModel = model_file_path

# Initialize conversation history in a global variable (similar to session state in Streamlit)
conversation_history = [{"role": "system", "content": "You are now chatting with a language model!"}]

# Function to generate a response
def generate_response(question_to_ask):
    global conversation_history
    # Append the user input to the conversation history
    conversation_history.append({"role": "user", "content": question_to_ask})
    
    # Call the Ollama API with the conversation history
    response = ollama.chat(model=desiredModel, messages=conversation_history)
    
    # Append the model's response to the conversation history
    model_response = response['message']['content']
    conversation_history.append({"role": "assistant", "content": model_response})
    return model_response

# Route for the home page where users can interact with the chatbot
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input.strip():  # Check if input is not empty
            generate_response(user_input)
        return redirect(url_for("home"))  # Refresh the page to display updated messages
    return render_template("home.html", messages=conversation_history)

# API endpoint to get chat history
@app.route("/api/messages", methods=["GET"])
def get_messages():
    """Fetch the entire conversation history."""
    return jsonify(conversation_history)

# API endpoint to send a question and receive a response
@app.route("/api/ask", methods=["POST"])
def api_ask():
    """Send a question to the model and receive its response."""
    data = request.get_json()  # Parse JSON data from the request
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request data"}), 400

    question = data["question"]
    if not question.strip():
        return jsonify({"error": "Question cannot be empty"}), 400

    # Generate a response using the function
    model_response = generate_response(question)
    return jsonify({"question": question, "response": model_response})
# To update a specific message in the conversation history by its index.
@app.route("/api/messages/<int:message_id>", methods=["PUT"])
def update_message(message_id):
    """Update a specific message in the conversation history."""
    data = request.get_json()  # Parse JSON data
    if not data or "content" not in data:
        return jsonify({"error": "Missing 'content' in request data"}), 400
    
    if 0 <= message_id < len(conversation_history):
        conversation_history[message_id]["content"] = data["content"]
        return jsonify({"message": "Message updated successfully", "updated_message": conversation_history[message_id]})
        
    else:
        return jsonify({"error": "Message ID out of range"}), 404

#     
@app.route("/api/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    """Delete a specific message in the conversation history."""
    if 0 <= message_id < len(conversation_history):
        deleted_message = conversation_history.pop(message_id)
        return jsonify({"message": "Message deleted successfully", "deleted_message": deleted_message})
    else:
        return jsonify({"error": "Message ID out of range"}), 404

if __name__ == "__main__":
    app.run(debug=True)