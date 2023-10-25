import os
import sys

from flask import Flask

sys.path.append(os.getcwd())

from mock.common_query.endpoint import common_query_blueprint

app = Flask(__name__)

app.register_blueprint(common_query_blueprint)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
