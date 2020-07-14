[![Build Status](https://travis-ci.com/Elfpkck/file-to-page.svg?branch=master)](https://travis-ci.com/Elfpkck/file-to-page) [![codecov](https://codecov.io/gh/Elfpkck/file-to-page/branch/master/graph/badge.svg)](https://codecov.io/gh/Elfpkck/file-to-page)
# Implementation of a test task described in `task.pdf`
## Running web application
1. Use interpreter: _python3.6+_
2. Create python virtual environment
3. Activate python virtual environment
4. Install third-party libs:\
`pip install -r requirements.txt`
5. From the project root:\
`python http_file_to_page.py`
6. For production use _nginx+gunicorn_ or something similar

## Running tests
1. Make sure you've done steps 1-4 from [Running web application](#running-web-application).\
2. From the project root:\
`python -m pytest tests`
