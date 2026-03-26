from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption 
from docling_surya import SuryaOcrOptions

class DoclingConverter:
    def __init__(self):
        pipeline_options = PdfPipelineOptions(
            do_ocr=True,
            ocr_model="suryaocr",
            allow_external_plugins=True,
            ocr_options=SuryaOcrOptions(lang=["en"], force_full_page_ocr=True, use_gpu=True),
            generate_picture_images=True,
            generate_table_images=True,
            do_formula_enrichment=True,
            do_picture_classification=True,
            do_code_enrichment=True,
            do_picture_description=True,
            do_chart_extraction=True,
            images_scale=1
        )
        
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
    def convert(self, in_file):
        return self.converter.convert(in_file)