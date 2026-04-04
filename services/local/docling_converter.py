from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption 
from docling_surya import SuryaOcrOptions
from docling.datamodel.accelerator_options import AcceleratorDevice

from interfaces import ParseInterface

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
            # code enrichment => requires VLM
            do_chart_extraction=False, # Requires granite
            do_picture_classification = False, # Requires Granite
            images_scale=1.0,
            do_table_structure=False,
            accelerator = AcceleratorDevice.CUDA,
            ocr_batch_size=48,
            layout_batch_size=48, 
        )
        
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
    def run(self, in_file):
        return self.converter.convert(in_file)