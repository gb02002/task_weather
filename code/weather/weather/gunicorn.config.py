import multiprocessing

#command = ""
bind = "0.0.0.0:8001"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 10
preload = True

loglevel = 'info'
limit_request_fields = 100
limit_request_fields_size = 8192
#raw_env = ""

