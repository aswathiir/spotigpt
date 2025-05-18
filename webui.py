from flask import Flask, render_template, request, jsonify
from app import EnhancedMusicChatbot  # Import your existing chatbot

app = Flask(__name__)
bot = EnhancedMusicChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    response = bot.generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)