import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'students.json')

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_students(students):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    students = load_students()
    return render_template('index.html', students=students)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "student": "2412111016"})

@app.route('/api/students', methods=['GET'])
def get_students():
    students = load_students()
    lop = request.args.get('lop')
    if lop:
        students = [s for s in students if s.get('lop') == lop]
    return jsonify(students)

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    students = load_students()
    for s in students:
        if s.get('id') == student_id:
            return jsonify(s)
    return jsonify({"error": "Student not found"}), 404

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json() or {}
    ten = data.get('ten')
    lop = data.get('lop')
    diem = data.get('diem')

    if not ten or not lop or diem is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        diem_float = float(diem)
        if diem_float < 0 or diem_float > 10:
            return jsonify({"error": "Diem must be between 0 and 10"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Diem must be a number"}), 400

    students = load_students()
    new_id = max([s.get('id', 0) for s in students], default=0) + 1
    new_student = {
        "id": new_id,
        "ten": ten,
        "lop": lop,
        "diem": diem_float
    }
    students.append(new_student)
    save_students(students)

    return jsonify(new_student), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
