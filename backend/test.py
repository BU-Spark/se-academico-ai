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
        
        import pytest
from search import clean_name

def test_clean_name_truncates_to_max_length():
    # Test input longer than max_length
    name = 'A' * 100  # 100 characters
    max_length = 50
    expected = 'A' * max_length
    assert clean_name(name, max_length) == expected

def test_clean_name_no_changes_needed():
    # Test input with no invalid characters and within max_length
    name = 'ValidName'
    expected = 'ValidName'
    assert clean_name(name) == expected

def test_clean_name_empty_string():
    # Test empty input
    name = ''
    expected = ''
    assert clean_name(name) == expected
    