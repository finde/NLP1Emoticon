from flask import Blueprint, jsonify
from Code.FeatureExtract import feature_dictionary

general = Blueprint('general', __name__)


@general.route('/getAllFeatures')
def getAllFeatures():
    return jsonify(feature_dictionary)


@general.route('/register')
def register():
    return jsonify({'success': 'True'})

@general.route('/index')
def index():
    return jsonify({'success': 'True'})