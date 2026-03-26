import sys

from ssh import docling_ssh

service = ""
if len(sys.argv) > 1:
    service = sys.argv[1]
    
if service == 'docling':
    docling_ssh.run()

sys.exit()