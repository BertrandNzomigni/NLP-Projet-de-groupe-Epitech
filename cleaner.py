import re

START_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK"
END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK"

def clean(text):
    #remove Project Gutenberg header
    position = 0
    for line in text:
        if line.startswith(START_MARKER):
            break
        position += 1
    text = text[position + 1:]

    #remove leading empty lines
    while text and text[0] == '\n':
        text.pop(0)

    #remove Project Gutenberg footer
    position = 0
    for line in text:
        if line.startswith(END_MARKER):
            break
        position += 1
    text = text[:position]

    #remove trailing empty lines
    while text and text[-1] == '\n':
        text.pop()

    return text


def normalize_spaces(text):
    content = []
    for line in text:
        #replace typographic ellipsis "x. . .y" with a single space
        line = re.sub(r"\.\s\.\s\.", " ", line)
        #replace multiple spaces/tabs with a single space
        line = re.sub(r"[ _\t]+", " ", line)
        content.append(line)
    return content