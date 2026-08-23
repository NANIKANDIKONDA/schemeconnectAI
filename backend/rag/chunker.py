import re


def chunk_document(document: str) -> list[str]:
    """
    Split a scheme document into meaningful semantic chunks.

    The document is divided based on section headings such as:
    Category, Description, Eligibility, Benefits,
    Documents Required, How to Apply, and Official Source.
    """

    if not document or not document.strip():
        return []

    # Normalize line endings and remove unnecessary spaces
    document = document.replace("\r\n", "\n").replace("\r", "\n").strip()

    # Split using blank lines
    sections = re.split(r"\n\s*\n", document)

    chunks = []

    for section in sections:
        section = section.strip()

        if section:
            chunks.append(section)

    return chunks