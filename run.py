from multiprocessing import Process
from bottle import run
from bottles import pdf_parse, file_share  # manually import your bottles

# Each tuple: (Bottle app, port)
bottles_to_run = [
    (pdf_parse.app, 8080),
    (file_share.app, 8081)
]

processes = []

for app, port in bottles_to_run:
    p = Process(target=run, kwargs={
        "app": app,
        "host": "localhost",
        "port": port,
        "server": "wsgiref"
    })
    p.start()
    print(f"Started {app} on port {port} as process {p.pid}")
    processes.append(p)

# Wait for all processes
for p in processes:
    p.join()