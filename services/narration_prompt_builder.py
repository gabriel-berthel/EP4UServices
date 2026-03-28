# service/narration_prompt_service.py

from typing import List, Tuple
import re

def contains_reference(text: str, ref_prefix: str, ref_num: int) -> bool:
    """
    Checks if `text` contains a reference with a specific prefix and number.

    Examples:
        - ref_prefix="Table", ref_num=2
        - ref_prefix="Tab", ref_num=3
        - ref_prefix="Fig", ref_num=1

    Handles cases like:
        - 'Table 2'
        - 'Table 2, 3'
        - 'Tab 1, 2, 3'

    Does NOT match:
        - 'Table 21' when looking for Table 2
    """
    # Build regex pattern dynamically
    # \b → word boundary
    # \s+ → one or more spaces
    # (?:\s*,\s*\d+)* → optionally match ', 3' etc.
    pattern = rf"\b{re.escape(ref_prefix)}\s+{ref_num}\b(?:\s*,\s*\d+)*"
    return bool(re.search(pattern, text))

class NarrationPromptBuilder:
    """Builds system and user prompts for TTS narration from scientific articles."""

    # (identifier, caption) tuples
    def __init__(self, tables: List[Tuple[str, str, str]], figures: List[Tuple[str, str, str]], footnotes: List[Tuple[str, str]]):
        
        self.tables = tables
        self.figures = figures
        self.footnotes = footnotes    
        
    def _format_list(self, item_list):   
        
        if item_list:
            self.tables_list = " - " + "\n\n - ".join(i for i in item_list)
        
        return "None"
    
    def build_system_prompt(self) -> str:
        return SYSTEM

    def build_user_prompt(self, chunk_text: str) -> str:

        chunk_mentions = []    
        chunk_footnotes = []
        
        for prefix, identifier, caption in self.tables + self.figures:
            if contains_reference(chunk_text, prefix, identifier):
                chunk_mentions.append(caption)
        
        for identifier, caption in self.footnotes:
            if identifier in chunk_text:
                chunk_footnotes.append(caption)
        
        return USER_BASE.format(
            chunk_text=chunk_text,
            mentions=self._format_list(chunk_mentions),
            footnotes=self._format_list(chunk_footnotes)
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
Candidate mentions:
{mentions}

Candidate footnotes:
{footnotes}

Process step-by-step, inserting SHOW/HIGHLIGHT markers as appropriate.
Include footnotes, tables, figure captions only if they help comprehension.
Output JSON with key "TTSChunks", ready for TTS playback.
"""