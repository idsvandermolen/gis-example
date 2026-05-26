import multiprocessing

wsgi_app = "backend.wsgi:application"
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = "info"
bind = "0.0.0.0:8000"
