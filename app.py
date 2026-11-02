import json
import os
from datetime import date
from flask import Flask, request, redirect, jsonify, render_template_string

app = Flask(__name__)

DATA_FILE = 'data.json'


def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {'students': [], 'attendance': {}}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    data = load_data()
    return render_template_string(INDEX_HTML, students=data['students'])


@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name', '').strip()
    if name:
        data = load_data()
        if name not in data['students']:
            data['students'].append(name)
            save_data(data)
    return redirect('/')


@app.route('/remove_student/<name>', methods=['POST'])
def remove_student(name):
    data = load_data()
    if name in data['students']:
        data['students'].remove(name)
        for day in data['attendance']:
            data['attendance'][day].pop(name, None)
        save_data(data)
    return redirect('/')


@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = load_data()
    today = str(date.today())
    if today not in data['attendance']:
        data['attendance'][today] = {}
    for student in data['students']:
        key = f'attendance_{student}'
        status = request.form.get(key, 'absent').strip().lower()
        data['attendance'][today][student] = status if status in ('present', 'absent') else 'absent'
    save_data(data)
    return redirect('/records')


@app.route('/records')
def view_records():
    data = load_data()
    return render_template_string(RECORDS_HTML, attendance=data['attendance'])


@app.route('/api/students')
def api_students():
    data = load_data()
    return jsonify(data['students'])


@app.route('/api/attendance')
def api_attendance():
    data = load_data()
    return jsonify(data['attendance'])


INDEX_HTML = """
<!doctype html>
<title>Attendance Tracker</title>
<h1>Attendance Tracker</h1>
<form method="post" action="/add_student">
  <input name="name" placeholder="Student name">
  <button type="submit">Add</button>
</form>
<h2>Students</h2>
<ul>
{% for s in students %}
  <li>{{ s }}
    <form method="post" action="/remove_student/{{ s }}" style="display:inline">
      <button type="submit">Remove</button>
    </form>
  </li>
{% endfor %}
</ul>
<form method="post" action="/attendance">
{% for s in students %}
  <div>{{ s }}: <select name="attendance_{{ s }}"><option value="present">present</option><option value="absent">absent</option></select></div>
{% endfor %}
<button type="submit">Mark Attendance</button>
</form>
"""

RECORDS_HTML = """
<!doctype html>
<title>Records</title>
<h1>Attendance Records</h1>
{% for day, records in attendance.items() | sort %}
<h2>{{ day }}</h2>
<ul>
{% for student, status in records.items() %}
  <li>{{ student }}: {{ status }}</li>
{% endfor %}
</ul>
{% endfor %}
"""


if __name__ == '__main__':
    app.run(debug=True)
