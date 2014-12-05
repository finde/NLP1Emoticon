import json
from flask import Blueprint, jsonify, Response
from Code.FeatureExtract import feature_dictionary

perceptron = Blueprint('perceptron', __name__)


@perceptron.route('/getAllFeatures')
def getAllFeatures():
    return Response(json.dumps(feature_dictionary), mimetype='application/json')


@perceptron.route('/train')
def train():
    return jsonify({'success': 'True'})


@perceptron.route('/predict')
def predict():
    return jsonify({'success': 'True'})