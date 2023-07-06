from flask import Flask, render_template, jsonify, request
import subprocess
import logging
import json

# Configure the logger
logging.basicConfig(level=logging.INFO)

# Create a formatter for JSON logs
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger_name': record.name,
            'module': record.module,
            'func_name': record.funcName,
        }
        return json.dumps(log_data)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

json_formatter = JsonFormatter()
console_handler.setFormatter(json_formatter)

logger.addHandler(console_handler)

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

@app.route('/execute', methods=['POST'])
def execute_curl():
    logger.info("starting curl execution")
    curl_string = request.form['curlString']
    curl_string = curl_string.replace('\n', '').replace('\\', '')

    logger.info(curl_string)
    # Execute the cURL command and get the result
    result = execute_curl(curl_string)

    logger.info(result)
    # Return the result as JSON response
    return jsonify(result=result)

def execute_curl(curl_command):
    try:
        result = subprocess.check_output(curl_command, shell=True, stderr=subprocess.STDOUT)
        logger.info("raw result: " + result.decode('utf-8'))
        return remove_characters_before_brace(result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        logger.error(f'Error executing curl command: {e.output.decode("utf-8")}')
        return f'Error executing curl command: {e.output.decode("utf-8")}'

if __name__ == '__main__':
    app.run()
