import os
import sqlite3
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, make_response
from random import choice

# App setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
DB_PATH = os.path.join(os.path.dirname(__file__), 'travel.db')

CONTINENTS = [
    'Asia', 'Europe', 'Africa', 'North America', 'South America', 'Australia', 'Antarctica'
]
CATEGORIES = ['Beach', 'Mountain', 'City', 'Desert', 'Nature', 'Cultural']
PRIORITIES = ['High', 'Medium', 'Low']


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS places (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               country TEXT NOT NULL,
               continent TEXT NOT NULL,
               category TEXT NOT NULL,
               description TEXT NOT NULL,
               priority TEXT NOT NULL,
               visited INTEGER NOT NULL DEFAULT 0,
               visited_date TEXT
           )'''
    )
    conn.commit()
    conn.close()


@app.context_processor
def inject_globals():
    return dict(CONTINENTS=CONTINENTS, CATEGORIES=CATEGORIES, PRIORITIES=PRIORITIES, datetime=datetime)


@app.route('/')
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) AS c FROM places')
    total = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) AS c FROM places WHERE visited=1')
    visited = cur.fetchone()['c']
    yet = total - visited
    conn.close()
    return render_template('home.html', total=total, visited=visited, yet=yet)


@app.route('/add', methods=['GET', 'POST'])
def add_place():
    if request.method == 'POST':
        form = request.form
        required = ['name', 'country', 'continent', 'category', 'description', 'priority']
        if not all(form.get(f) for f in required):
            flash('All fields are required.', 'danger')
            return render_template('add_place.html')
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO places (name, country, continent, category, description, priority, visited) VALUES (?, ?, ?, ?, ?, ?, 0)',
            (
                form['name'].strip(),
                form['country'].strip(),
                form['continent'],
                form['category'],
                form['description'].strip(),
                form['priority']
            )
        )
        conn.commit()
        conn.close()
        flash('Place added to your bucket list!', 'success')
        return redirect(url_for('places'))
    return render_template('add_place.html')


def build_filters_query(args):
    clauses = []
    params = []
    if args.get('continent'):
        clauses.append('continent = ?')
        params.append(args['continent'])
    if args.get('category'):
        clauses.append('category = ?')
        params.append(args['category'])
    status = args.get('status')
    if status == 'visited':
        clauses.append('visited = 1')
    elif status == 'not_visited':
        clauses.append('visited = 0')
    search = args.get('search', '').strip()
    if search:
        clauses.append('(LOWER(name) LIKE ? OR LOWER(country) LIKE ?)')
        like = f"%{search.lower()}%"
        params.extend([like, like])
    where = (' WHERE ' + ' AND '.join(clauses)) if clauses else ''
    return where, params


@app.route('/places')
def places():
    conn = get_db()
    cur = conn.cursor()
    where, params = build_filters_query(request.args)

    sort = request.args.get('sort', '')
    order = ' ORDER BY '
    if sort == 'priority':
        # High > Medium > Low
        order += "CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, name ASC"
    else:
        order += 'id DESC'

    # Simple pagination
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    per_page = 10
    offset = (page - 1) * per_page

    cur.execute(f'SELECT COUNT(*) AS c FROM places{where}', params)
    total = cur.fetchone()['c']

    cur.execute(
        f'SELECT * FROM places{where}{order} LIMIT ? OFFSET ?',
        (*params, per_page, offset)
    )
    rows = cur.fetchall()
    conn.close()

    return render_template('places.html', places=rows, total=total, page=page, per_page=per_page)


@app.route('/edit/<int:pid>', methods=['GET', 'POST'])
def edit_place(pid):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        form = request.form
        required = ['name', 'country', 'continent', 'category', 'description', 'priority']
        if not all(form.get(f) for f in required):
            flash('All fields are required.', 'danger')
        else:
            cur.execute(
                'UPDATE places SET name=?, country=?, continent=?, category=?, description=?, priority=? WHERE id=?',
                (
                    form['name'].strip(),
                    form['country'].strip(),
                    form['continent'],
                    form['category'],
                    form['description'].strip(),
                    form['priority'],
                    pid
                )
            )
            conn.commit()
            flash('Place updated.', 'success')
            conn.close()
            return redirect(url_for('places'))
    cur.execute('SELECT * FROM places WHERE id=?', (pid,))
    row = cur.fetchone()
    conn.close()
    if not row:
        flash('Place not found.', 'warning')
        return redirect(url_for('places'))
    return render_template('edit_place.html', place=row)


@app.route('/delete/<int:pid>', methods=['POST'])
def delete_place(pid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM places WHERE id=?', (pid,))
    conn.commit()
    conn.close()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'ok': True})
    flash('Place deleted.', 'success')
    return redirect(url_for('places'))


@app.route('/toggle_visited/<int:pid>', methods=['POST'])
def toggle_visited(pid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT visited FROM places WHERE id=?', (pid,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({'ok': False, 'error': 'Not found'}), 404
    new_val = 0 if row['visited'] else 1
    vdate = date.today().isoformat() if new_val == 1 else None
    cur.execute('UPDATE places SET visited=?, visited_date=? WHERE id=?', (new_val, vdate, pid))
    conn.commit()
    conn.close()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'ok': True, 'visited': bool(new_val), 'visited_date': vdate})
    return redirect(url_for('places'))


@app.route('/api/stats')
def api_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) AS total FROM places')
    total = cur.fetchone()['total']
    cur.execute('SELECT COUNT(*) AS v FROM places WHERE visited=1')
    visited = cur.fetchone()['v']
    cur.execute('SELECT continent, COUNT(*) AS c FROM places GROUP BY continent')
    by_continent = {row['continent']: row['c'] for row in cur.fetchall()}
    conn.close()
    not_visited = total - visited
    return jsonify({
        'total': total,
        'visited': visited,
        'not_visited': not_visited,
        'by_continent': by_continent,
        'completion_pct': (visited / total * 100) if total else 0
    })


@app.route('/stats')
def stats_page():
    return render_template('stats.html')


@app.route('/export.csv')
def export_csv():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM places ORDER BY id ASC')
    rows = cur.fetchall()
    conn.close()
    lines = [
        'id,name,country,continent,category,description,priority,visited,visited_date'  # header
    ]
    for r in rows:
        # naive CSV escaping by replacing commas in text fields
        def esc(x):
            if x is None:
                return ''
            s = str(x).replace('\n', ' ').replace('\r', ' ')
            if ',' in s or '"' in s:
                s = '"' + s.replace('"', '""') + '"'
            return s
        lines.append(','.join([
            str(r['id']), esc(r['name']), esc(r['country']), esc(r['continent']), esc(r['category']),
            esc(r['description']), esc(r['priority']), str(r['visited']), esc(r['visited_date'])
        ]))
    csv_data = '\n'.join(lines)
    resp = make_response(csv_data)
    resp.headers['Content-Type'] = 'text/csv'
    resp.headers['Content-Disposition'] = 'attachment; filename=places.csv'
    return resp


@app.route('/random')
def random_destination():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM places')
    rows = cur.fetchall()
    conn.close()
    if not rows:
        flash('Your list is empty. Add a place first!', 'warning')
        return redirect(url_for('add_place'))
    r = choice(rows)
    flash(f"Random pick: {r['name']} in {r['country']} ({r['continent']})", 'info')
    return redirect(url_for('places', search=r['name']))


@app.route('/timeline')
def timeline():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM places WHERE visited=1 AND visited_date IS NOT NULL ORDER BY visited_date DESC')
    rows = cur.fetchall()
    conn.close()
    return render_template('timeline.html', places=rows)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
