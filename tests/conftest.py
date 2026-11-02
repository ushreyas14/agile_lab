import pytest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app

@pytest.fixture
def app(tmp_path):
    flask_app.config['TESTING'] = True
    test_data_file = str(tmp_path / 'test_data.json')

    import app as app_module
    original_data_file = app_module.DATA_FILE
    app_module.DATA_FILE = test_data_file

    yield flask_app

    app_module.DATA_FILE = original_data_file
    if os.path.exists(test_data_file):
        os.remove(test_data_file)

@pytest.fixture
def client(app):
    return app.test_client()
