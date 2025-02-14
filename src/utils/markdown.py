from markdown_it import MarkdownIt


def split_markdown(markdown_text: str, chunk_size: int | None = None) -> list[str]:
    """
    Parse markdown text into sections and create chunks based on size limit.

    Args:
        markdown_text (str): Input markdown text
        chunk_size (int): Maximum size of each chunk

    Returns:
        List[str]: List of text chunks
    """
    # Parse markdown into sections
    md = MarkdownIt()
    tokens = md.parse(markdown_text)

    # Extract sections with proper heading levels
    sections = []
    current_section = []

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.type == "heading_open":
            # Save previous section if it exists
            if current_section:
                sections.append("".join(current_section))
                current_section = []

            # Get heading level and text
            level = len(token.markup)  # number of '#' characters
            heading_text = tokens[i + 1].content

            # Add heading with proper number of hashtags
            current_section.append("#" * level + " " + heading_text + "\n")
            i += 2  # Skip the heading_content and heading_close tokens

        elif token.type == "inline" and tokens[i - 1].type != "heading_open":
            current_section.append(token.content + "\n")
            i += 1
        else:
            i += 1

    # Add final section if it exists
    if current_section:
        sections.append("".join(current_section))

    if chunk_size:
        current_part = ""
        result = []
        for section in sections:
            new_section = current_part + "\n" + section
            if len(new_section) < chunk_size:
                current_part = new_section
            else:
                result.append(current_part)
                current_part = ""
        return result

    return sections
