from flask import Flask, request
from flask_cors import CORS
import psutil
from llama_cpp import Llama  # Assuming llama_cpp is the module for Llama

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

def print_memory_usage():
	process = psutil.Process()
	mem_info = process.memory_info()
	print(f"Memory Usage: {mem_info.rss / (1024 ** 2):.2f} MB")

model_name = "./Qwen2.5-0.5B-Instruct-IQ4_XS.gguf"
llm = Llama(model_path=model_name, chat_format="chatml")  # Set chat_format according to the model you are using



@app.route('/send_message', methods=['POST'])
def send_message():
	print("Received a message")
	data = request.get_json()
	user_message = data.get("message", "")
	system_prompt = data.get("system_prompt", "You are a great storyteller that create a story for user")
	messages = [
		{"role": "system", "content": system_prompt},
		{"role": "user", "content": user_message}
	]
	print(messages)
	print_memory_usage()
	response = llm.create_chat_completion(
		messages=messages,
		stream=True,
		max_tokens=1024,
		repeat_penalty=2,
		temperature=0.4,
		top_p=0.9,
		top_k=20,
		min_p=0.02,
	)
	
	def generate():
		response_str = ""
		for chunk in response:
			for key in chunk["choices"][0]["delta"]:
				if key == "content":
					string = chunk["choices"][0]['delta'][key]
					response_str += string
					yield f"{string}"
		print_memory_usage()
		print(response_str)
	
	return app.response_class(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
	app.run(debug=False, host='localhost', port=5000)
