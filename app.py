from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

students = []

HTML = """

<!DOCTYPE html>

<html>
<head>
    <title>Student Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background: #f4f6f9;
        }
        h1 { color: #243b55; }
        form, .student {
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
        }
        input, button {
            padding: 10px;
            margin: 5px 0;
        }
        button {
            background: #243b55;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Student Management System</h1>

<form action="/add" method="post">
    <h3>Add a Student</h3>
    <input name="roll" placeholder="Roll Number" required>
    <input name="name" placeholder="Student Name" required>
    <input name="course" placeholder="Course" required>
    <button type="submit">Add Student</button>
</form>

<h2>Student Records</h2>

{% for student in students %}
<div class="student">
    <strong>{{ student.roll }} — {{ student.name }}</strong>
    <p>Course: {{ student.course }}</p>
    <form action="/delete/{{ student.roll }}" method="post">
        <button type="submit">Delete</button>
    </form>
</div>
{% else %}
<p>No students added yet.</p>
{% endfor %}

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, students=students)

@app.route("/add", methods=["POST"])
def add_student():
    roll = request.form["roll"].strip()
    name = request.form["name"].strip()
    course = request.form["course"].strip()

    if not roll or not name or not course:
        return "All fields are required.", 400

    if any(s["roll"] == roll for s in students):
        return "Roll number already exists.", 400

    students.append({
    "roll": roll,
    "name": name,
    "course": course
})

    return redirect(url_for("home"))

@app.route("/delete/<roll>", methods=["POST"])
def delete_student(roll):
    students[:] = [s for s in students if s["roll"] != roll]
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
