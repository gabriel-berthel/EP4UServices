
"""

Expects a bunch of PDFs in in_folder, 
process them thru docling, 
and picke them in out_folder as the hash of the initial file content.

Handle every file since I can't know which one was uploaded.

"""

from core.docling_converter import DoclingConverter
import os
import hashlib
import pickle

in_folder = os.environ['IN_FOLDER']
out_folder = os.environ['OUT_FOLDER']

unprocessed = [f for f in os.listdir(in_folder) if os.path.isfile(os.path.join(in_folder, f))]

converter = DoclingConverter()

for pdf in unprocessed: 
    with open(pdf, 'rb') as f:
        pdf_hash = hashlib.sha256(f.read()).digest()
        
    os.remove(pdf)
    
    results =  converter.convert(pdf)
    
    out_file = os.path.join(out_folder, pdf_hash)
    
    with open(out_file, 'wb') as f:
        pickle.dump(results, f)
    
