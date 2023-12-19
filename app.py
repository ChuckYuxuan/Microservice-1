from flask import Flask, render_template, request, jsonify, redirect
from flask_graphql import GraphQLView

from dbconnector import get_db_conn, close_conn, init_db, mock_data
from resources.score_resource import ScoreResource
from resources.graphql_schema import schema

app = Flask(__name__)
instance = ScoreResource()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/dashboard/async_search_student', methods=['GET', 'POST'])
async def search_student_async():
    if request.method == 'POST':
        id = request.form.get('student_id')
        result = await instance.get_score_async(id)
        if result:
            return render_template('search_student.html', results=result['score']['score'], info=result['student']['student'])

    return render_template('search_student.html')


@app.route('/api/dashboard/sync_search_student', methods=['GET', 'POST'])
async def search_student_sync():
    if request.method == 'POST':
        id = request.form.get('student_id')
        result = await instance.get_score_sync(id)
        if result:
            return render_template('search_student.html', results=result['score']['score'], info=result['student']['student'])

    return render_template('search_student.html')

@app.route('/get_score_info_json/<id>')
def get_score_info(id):
    conn = get_db_conn()
    result = conn.execute(f"SELECT * FROM scores WHERE student_id = {id}")
    score = result.fetchall()
    close_conn(conn)
    return jsonify({'score': score})


@app.route('/get_student_info_json/<id>')
def get_student_json(id):
    conn = get_db_conn()
    result = conn.execute(f"SELECT * FROM students WHERE student_id = '{id}'")
    student = result.fetchone()
    close_conn(conn)
    return jsonify({'student': student})


@app.route('/insert_scores', methods=['POST'])
def add_score():
    student_id = request.json.get('student_id')
    student_name = request.json.get('student_name')
    course_id = request.json.get('course_id')
    course_name = request.json.get('course_name')
    score = request.json.get('score')

    conn = get_db_conn()
    conn.execute(f"INSERT INTO students VALUES ({student_id}, '{student_name}')")
    conn.execute(f"INSERT INTO scores VALUES ({student_id}, '{student_name}', {course_id}, '{course_name}', {score})")
    close_conn(conn)

    return '', 201


@app.route('/api/dashboard/view_score')
def view_score():
    return render_template('view_score.html')


@app.route('/average_scores', methods=['POST'])
def get_average_scores():
    course_id = request.json.get('course_id')

    conn = get_db_conn()
    result = conn.execute(f"SELECT year, AVG(score) FROM history_scores WHERE course_id = {course_id} GROUP BY year")
    scores = result.fetchall()
    conn.close()

    return jsonify(scores)

# use graphql to search student scores
app.add_url_rule('/api/dashboard/graphql_search_student', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

# query example, where id is "student_id"
# {
#   avgscores(id: "3") {
#     id
#     avgscore
#   }
# }

if __name__ == '__main__':
    init_db()
    mock_data()
    app.run(host='0.0.0.0', port=5000)
