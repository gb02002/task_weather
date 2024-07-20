import multiprocessing

#command = ""
#pythonpath = "/home/jay/Desktop/python/orgproj/"
bind = "127.0.0.1:8001"
workers = multiprocessing.cpu_count() * 2 + 1
limit_request_fields = 100
limit_request_fields_size = 8192
#raw_env = ""

