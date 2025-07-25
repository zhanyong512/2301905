from flask import Flask, request, redirect, url_for, render_template_string
import re

app = Flask(__name__)

home_template = '''
<!DOCTYPE html>
<html>
<head><title>Search</title></head>
<body>
    <h1>Search</h1>
    <form method="post">
        <input type="text" name="term" value="" required>
        <input type="submit" value="Submit">
    </form>
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

result_template = '''
<!DOCTYPE html>
<html>
<head><title>Result</title></head>
<body>
    <h1>Search Result</h1>
    <p>You searched for: <strong>{{ term }}</strong></p>
    <a href="{{ url_for('home') }}"><button>Back to Home</button></a>
</body>
</html>
'''

def is_xss(input_text):
    return bool(re.search(r'<[^>]*script[^>]*>', input_text, re.IGNORECASE))

def is_sql_injection(input_text):
    return bool(re.search(r"(--)|([';]+)|(union\s+select)", input_text, re.IGNORECASE))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        term = request.form['term']
        if is_xss(term):
            return render_template_string(home_template, error="Potential XSS detected. Please try again.")
        elif is_sql_injection(term):
            return render_template_string(home_template, error="Potential SQL Injection detected. Please try again.")
        else:
            return redirect(url_for('result', term=term))
    return render_template_string(home_template)

@app.route('/result')
def result():
    term = request.args.get('term', '')
    return render_template_string(result_template, term=term)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
