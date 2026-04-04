from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption 
from docling_surya import SuryaOcrOptions
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from services.interfaces import ParseInterface


# Surya OCR pad_token_id patch
# Cuz newer versions of Docling > Transformers v5. Surya still on v4
tokenizer = AutoTokenizer.from_pretrained("vikp/surya_rec")
model = AutoModelForSeq2SeqLM.from_pretrained("vikp/surya_rec")

if getattr(model.config, "pad_token_id", None) is None:
    if tokenizer.pad_token_id is not None:
        model.config.pad_token_id = tokenizer.pad_token_id
    else:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = tokenizer.pad_token_id

class DoclingConverter(ParseInterface):
    def __init__(self):
        pipeline_options = PdfPipelineOptions(
        do_ocr=True,
            ocr_model="suryaocr",
            allow_external_plugins=True,
            ocr_options=SuryaOcrOptions(lang=["en"], force_full_page_ocr=True, use_gpu=True),
            generate_picture_images=True,
            generate_table_images=True,
            do_formula_enrichment=True,
            do_picture_description=False,
            # code enrichment => requires VLM
            do_chart_extraction=False, # Requires granite
            do_picture_classification = False, # Requires Granite
            images_scale=1.0,
            do_table_structure=False,
            accelerator_options = AcceleratorOptions(device=AcceleratorDevice.CUDA),
            ocr_batch_size=48,
            layout_batch_size=48, 
        )
        
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
    def run(self, path):
        return self.converter.convert(path)