from app.settings import LINE_WIDTH

def wrapper(s: str) -> str:
    """
    Wraps a given string to fit within a fixed width suitable for an 80mm printer.

    This function takes a string 's' and formats it so that each line does not exceed
    48 characters. This character limit is chosen based on the printing capabilities of an
    80mm printer, ensuring that the text is properly wrapped at word boundaries.

    The function splits the input string into words and accumulates them in a new string,
    inserting a newline character when adding another word would exceed the 48-character limit.
    If the string is shorter than or equal to 48 characters, a newline is simply appended.

    Args:
        s (str): The string to be wrapped for printing.

    Returns:
        str: The formatted string with newline characters inserted at appropriate positions.
    """
    n = len(s)
    count = 0
    new_s = ""
    
    # If the string exceeds the length limit, perform word wrapping.
    if n > 48:
        for word in s.split(' '):
            
            if (count + len(word) + 1) < 48:
                new_s += word + " "
                count += len(word) + 1  # Update the count with the length of the word and a space.
            else:
                new_s += "\n"
                count = 0
        new_s += '\n'
        return new_s
    # If the string is within the limit, simply append a newline at the end.
    s += "\n"
    return s

def calculated_space_between(left: str, right: str) -> str:
    """
    Creates a single line by aligning two strings with calculated spacing between them.

    This function takes two strings, 'left' and 'right', and returns a single string that fits
    within a fixed width defined by LINE_WIDTH. The function calculates the number of spaces needed 
    between the two strings so that the entire line reaches LINE_WIDTH. If there is not enough space 
    to fit both strings on the same line, the function breaks the line by placing the 'right' string 
    on a new line, right-justified within the fixed width.

    Args:
        left (str): The string to be placed on the left side of the line.
        right (str): The string to be placed on the right side of the line.

    Returns:
        str: A formatted string where 'left' and 'right' are separated by spaces to fill LINE_WIDTH,
             or 'right' is placed on a new line if necessary.
    """
    combined_length = len(left) + len(right)
    spaces_needed = LINE_WIDTH - combined_length

    # Very if enough space
    if spaces_needed > 0:
        line = left + (' ' * spaces_needed) + right
    else:
        line = left + '\n' + right.rjust(LINE_WIDTH)
    
    return line