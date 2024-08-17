from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = ''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply})
    except openai.error.RateLimitError:
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
