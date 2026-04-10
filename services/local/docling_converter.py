import os

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_surya import SuryaOcrOptions
from docling.datamodel.accelerator_options import AcceleratorDevice
from services.interfaces import ParseInterface

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
            accelerator = AcceleratorDevice.CUDA,
            ocr_batch_size=48,
            layout_batch_size=48
        )
        
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
            }
        )
    
        self.converter._get_pipeline(InputFormat.PDF)
        
    def run(self, path):
        return self.converter.convert(path)