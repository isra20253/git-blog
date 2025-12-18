import sys
try:
    import requests
    print('requests', requests.__version__)
except Exception as e:
    print('NOREQUESTS', e)
