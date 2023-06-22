from flask import Flask, render_template, jsonify, request
import subprocess

def remove_characters_before_brace(input_string):
    brace_index = input_string.find('{')
    if brace_index != -1:
        result = input_string[brace_index:]
    else:
        result = input_string
    return result

app = Flask(__name__)

# Health check endpoint
@app.route('/health')
def health_check():
    return 'OK'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_curl():
    curl_string = request.form['curlString']
    curl_string = curl_string.replace('\n', '').replace('\\', '')
    # Execute the cURL command and get the result
    result = execute_curl(curl_string)

    # Return the result as JSON response
    return jsonify(result=result)

def execute_curl(curl_command):
    try:
        result = subprocess.check_output(curl_command, shell=True, stderr=subprocess.STDOUT)
        return remove_characters_before_brace(result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        return f'Error executing curl command: {e.output.decode("utf-8")}'

if __name__ == '__main__':
    app.run()
