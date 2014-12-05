from flask import Blueprint, jsonify

auth = Blueprint('auth', __name__)


@auth.route('/authenticate')
def authenticate():
    return jsonify({'success': 'True'})


@auth.route('/register')
def register():
    return jsonify({'success': 'True'})
