from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

PAGE = """
<h2>Aegis Cloud Systems — Employee Directory</h2>
<form method="get" action="/search">
    <input name="name" placeholder="Search employee name...">
    <button type="submit">Search</button>
</form>
<table border="1" cellpadding="6">
<tr><th>ID</th><th>Name</th><th>Department</th><th>Email</th></tr>
{% for row in rows %}
<tr><td>{{row[0]}}</td><td>{{row[1]}}</td><td>{{row[2]}}</td><td>{{row[3]}}</td></tr>
{% endfor %}
</table>
"""

@app.route("/")
def home():
    return render_template_string(PAGE, rows=[])

@app.route("/search")
def search():
    name = request.args.get("name", "")
    conn = sqlite3.connect("company.db")
    cur = conn.cursor()
    # VULNERABLE: we use a string concatenation instead of a parameterized query
    query = "SELECT id, name, department, email FROM employees WHERE name LIKE '%" + name + "%'"
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except Exception as e:
        rows = [("ERR", str(e), "", "")]
    conn.close()
    return render_template_string(PAGE, rows=rows)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
