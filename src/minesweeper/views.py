# coding: utf-8

import random

from flask import session, url_for, redirect, render_template
from flask.ext.assets import Bundle

from .init import app, assets


assets.register('js_all', Bundle(
    'js/jquery-1.11.1.js',
    'js/bootstrap.js',
    'js/minesweeper.js',
    output='js/final/all.js'
))

assets.register('css_all', Bundle(
    'css/bootstrap-theme.css',
    'css/bootstrap.css',
    filters='jinja2',
    output='css/final/all.css'
))


field_presets = dict(
    beginner=dict(width=9, height=9, bombs=10),
    intermediate=dict(width=16, height=16, bombs=40),
    expert=dict(width=30, height=16, bombs=99),
    custom=dict(width=9, height=9, bombs=10),
)


def generate_new_field(width, height, bombs):
    """
    Generates new play field.
    """
    def increase(x, y):
        if x < 0 or y < 0: return
        try:
            game_field[y][x] += 1 if game_field[y][x] != 55 else 0
        except IndexError as e:
            pass

    game_field = [[10 for x in range(0, width)] for y in range(0, height)]
    b = 0
    while b < bombs:
        b_x = random.randint(0, width - 1)
        b_y = random.randint(0, height - 1)

        if game_field[b_y][b_x] != 55:
            game_field[b_y][b_x] = 55
            xy = [(xx, yy) for xx in range(b_x - 1, b_x + 2) for yy in range(b_y - 1, b_y + 2)]
            for i in xy: increase(i[0], i[1])
            b += 1

    return game_field


def clear_field():
    """
    Clears game field.
    """
    if 'field' in session:
        session.pop('field')


@app.route('/')
def index():
    if not session.get('field', []):
        print('session level', session.get('level'))
        params = session.get('field_presets', field_presets[session.get('level', 'beginner')])
        print('params', params)
        session['field'] = generate_new_field(**params)

    return render_template('index.html',
        game_field=session['field'],
        level=session.get('level', 'beginner'),
    )


@app.route('/new')
@app.route('/new/<string:level>')
def new_game(level=None):
    clear_field()

    level = level if level in field_presets else session.get('level', 'beginner')
    print('level', level)
    # TODO: Logic ???
    if 'field_presets' in session and field_presets[level] != session.get('field_presets'):
        session['field_presets'] = field_presets[level]
        session['level'] = level

    return redirect(url_for('.index'))


@app.route('/click', methods=['POST'])
def cell_click():
    pass


# SYSTEM NEEDED FUNCTIONS

@app.errorhandler(401)
def not_authorized(error):
    return render_template('401.html', error=error), 401


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', error=error), 500


@app.errorhandler(501)
def not_implemented(error):
    return render_template('501.html', error=error), 501
