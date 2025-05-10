# backend/pdf_conversion.py

'''
This python script is intended to convert pdfs to markdown for better performance
'''
import pymupdf4llm
import pathlib
from pathlib import Path
import aiofiles
import asyncio

async def convert_pdfs_to_markdown(paper, output_folder_path):


    print(f"Processing {paper}")

    paper = Path(paper)

    # convert the PDF to markdown

    md_text = pymupdf4llm.to_markdown(str(paper))

    # Save with same name but in markdown_papers folder
    output_file = output_folder_path / f"{paper.stem}.md"  # stem is the filename without the extension
    # now work with the markdown text, e.g. store as a UTF8-encoded file

    # pathlib.Path(output_file).write_bytes(md_text.encode())
    # Use aiofiles to write the markdown asynchronously
    async with aiofiles.open(output_file, 'w') as f:
        await f.write(md_text)
    print(f"Saved {output_file}")