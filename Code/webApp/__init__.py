from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/averaged-multiclass-perceptron')
    def amp():
        # TODO: make an API to show the demo
        return render_template('amp.html')

    @app.route('/hidden-markov-model')
    def hmm():
        return render_template('hmm.html')


    return app

if __name__ == '__main__':
    create_app().run(debug=True)