import pytest
from unittest.mock import patch
from pathlib import Path
from pdf_conversion import convert_pdfs_to_markdown

@pytest.mark.asyncio
async def test_convert_pdfs_to_markdown():
    # Mock inputs
    paper_path = "test_paper.pdf"
    output_folder_path = Path("markdown_papers")
    markdown_content = "# Mock Markdown Content"

    # Mock the `pymupdf4llm.to_markdown` function
    with patch("pymupdf4llm.to_markdown", return_value=markdown_content) as mock_to_markdown, \
         patch("aiofiles.open", autospec=True) as mock_aiofiles:
        # Call the function
        await convert_pdfs_to_markdown(paper_path, output_folder_path)

        # Assertions
        mock_to_markdown.assert_called_once_with(str(paper_path))
        mock_aiofiles.assert_called_once_with(output_folder_path / "test_paper.md", "w")
        mock_aiofiles.return_value.__aenter__.return_value.write.assert_called_once_with(markdown_content)