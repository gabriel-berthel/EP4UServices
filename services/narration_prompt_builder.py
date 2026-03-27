# service/narration_prompt_service.py

from typing import Dict

class NarrationPromptBuilder:
    """Builds system and user prompts for TTS narration from scientific articles."""

    @staticmethod
    def build_system_prompt() -> str:
        return SYSTEM

    @staticmethod
    def build_user_prompt(input_data: Dict, optional_instructions: str = "") -> str:
        
        tables_list = "\n".join(f"{k}: {v}" for k, v in input_data['tables'].items()) or "None"
        figures_list = "\n".join(f"{k}: {v}" for k, v in input_data['figures'].items()) or "None"
        footnotes_list = "\n".join(f"{k}: {v}" for k, v in input_data['footnotes'].items()) or "None"

        
        return USER_BASE.format(
            chunk_text=input_data['chunk_text'],
            tables=tables_list,
            figures=figures_list,
            footnotes=footnotes_list,
            instructions=optional_instructions
        )


SYSTEM = """
You are an expert academic lecturer and professional speech narrator.

Convert scientific article text into TTS-ready spoken prose, closely following the source material. Narration should sound natural, like a professor explaining the content aloud, while remaining faithful to the text’s meaning, flow, and technical detail.

Rules and Style:
- Output JSON with a single key "TTSChunks", whose value is an array of strings.
- Maintain headings to guide narrative flow.
- Explain math only when necessary.
- Use markers:
  <<SHOW_TABLE ID>>, <<SHOW_FIGURE ID>>, <<HIGHLIGHT_TABLE ID>>, <<HIGHLIGHT_FIGURE ID>>, <<SHOW_FOOTNOTE ID>>, <<HIGHLIGHT_FOOTNOTE ID>>
- Multiple references may be comma-separated: <<SHOW_TABLE 3,5>>
- Include footnotes, tables, figure captions only if they aid comprehension.
- Avoid expanding large tables or figures inline.
- Keep narration faithful to the original text and natural for TTS.
- Each chunk must be smooth, readable aloud, and self-contained.
"""

USER_BASE = """
Here is the article content to convert into TTS chunks:

{chunk_text}

Reference sheet:
Tables:
{tables}

Figures:
{figures}

Footnotes:
{footnotes}

Instructions:
{instructions}

Process step-by-step, inserting SHOW/HIGHLIGHT markers as appropriate.
Include footnotes, tables, figure captions only if they help comprehension.
Output JSON with key "TTSChunks", ready for TTS playback.
"""