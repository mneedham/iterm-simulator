import iterm2
import asyncio
import re
from markdown_it import MarkdownIt

keyboard_shortcuts = {
    "Ctrl+A": '\x01',  # Move to the beginning of the line
    "Ctrl+B": '\x02',  # Move backward one character
    "Ctrl+C": '\x03',  # Interrupt (send SIGINT to) the current process
    "Ctrl+D": '\x04',  # Delete the character under the cursor (EOF if line is empty)
    "Ctrl+E": '\x05',  # Move to the end of the line
    "Ctrl+F": '\x06',  # Move forward one character
    "Ctrl+G": '\x07',  # Bell (beep)
    "Ctrl+H": '\x08',  # Backspace (same as the backspace key)
    "Ctrl+I": '\x09',  # Tab (same as the Tab key)
    "Ctrl+J": '\x0a',  # Newline (same as the Enter/Return key)
    "Ctrl+K": '\x0b',  # Kill (cut) text from the cursor to the end of the line
    "Ctrl+L": '\x0c',  # Clear the screen
    "Ctrl+M": '\x0d',  # Carriage return (same as the Enter/Return key)
    "Ctrl+N": '\x0e',  # Move to the next line in history
    "Ctrl+O": '\x0f',  # Execute the current line and fetch the next line from history
    "Ctrl+P": '\x10',  # Move to the previous line in history
    "Ctrl+Q": '\x11',  # Resume transmission (used with software flow control)
    "Ctrl+R": '\x12',  # Reverse search in history
    "Ctrl+S": '\x13',  # Suspend transmission (used with software flow control)
    "Ctrl+T": '\x14',  # Transpose (swap) the character under the cursor with the one before it
    "Ctrl+U": '\x15',  # Kill (cut) text from the cursor to the beginning of the line
    "Ctrl+V": '\x16',  # Quoted insert (insert the next character verbatim)
    "Ctrl+W": '\x17',  # Kill (cut) the word before the cursor
    "Ctrl+X": '\x18',  # Used as a prefix for other shortcuts
    "Ctrl+Y": '\x19',  # Yank (paste) the most recently killed text
    "Ctrl+Z": '\x1a'   # Suspend the current process (send SIGTSTP)
}

# Example usage:
ctrl_l_sequence = keyboard_shortcuts["Ctrl+L"]

valid_prompts = [
    "$",
    ">>>",
    ">>> Send a message (/? for help)"
]

PROMPT_PATTERN = "$"  # Adjust this to match your shell's prompt
PYTHON_PROMPT_PATTERN = ">>>"

async def wait_for_prompt(session):
    await asyncio.sleep(0.5)  # short delay

    while True:
        # Get the session's screen contents
        screen_contents = await session.async_get_screen_contents()

        # Determine the number of lines
        num_lines = screen_contents.number_of_lines

        # Extract the lines from the screen contents
        lines_data = [screen_contents.line(i) for i in range(num_lines)]

        # Find the last non-empty line
        for line_data in reversed(lines_data):
            last_line = line_data.string.strip()
            if last_line:
                break

        print(f"Detected last line: [{last_line.strip()}]", last_line.strip() == PROMPT_PATTERN)

        if last_line.strip() in valid_prompts:
            break
        await asyncio.sleep(0.1)


async def simulated_typing(session, text, delay=0.1):
    for char in text:
        await session.async_send_text(char)
        await asyncio.sleep(delay)
    await session.async_send_text("\n")  # To execute the command after typing
    await wait_for_prompt(session)

async def find_or_create_session(app, window_index=None, tab_index=None):
    windows = app.windows
    if window_index is not None and 0 <= window_index < len(windows):
        window = windows[window_index]
    else:
        window = app.current_window
        if not window:
            window = await iterm2.Window.async_create(connection)

    tabs = window.tabs
    if tab_index is not None and 0 <= tab_index < len(tabs):
        tab = tabs[tab_index]
    else:
        tab = window.current_tab
        if not tab:
            tab = await window.async_create_tab()

    session = tab.current_session
    if not session:
        session = await tab.async_create_session()

    return session



# def extract_commands_from_md(file_path):
#     with open(file_path, 'r') as file:
#         content = file.read()

#     md = MarkdownIt()
#     tokens = md.parse(content)
#     commands = []

#     in_code_block = False
#     for token in tokens:
#         if token.type == "fence" and token.tag == "code":
#             commands.append(token.content.strip())

#     return commands

# def extract_commands_from_md(file_path):
#     with open(file_path, 'r') as file:
#         content = file.read()

#     md = MarkdownIt()
#     tokens = md.parse(content)
#     items = []

#     # Create a regular expression pattern for keyboard shortcuts using the dictionary keys
#     shortcut_pattern = r'\[(' + '|'.join(re.escape(key) for key in keyboard_shortcuts.keys()) + r')\]'
    
#     for token in tokens:
#         if token.type == "fence" and token.tag == "code":
#             items.append(token.content.strip())
#         elif token.type == "inline":
#             shortcut_match = re.match(shortcut_pattern, token.content)
#             if shortcut_match:
#                 items.append(shortcut_match.group(1))

#     return items

def extract_commands_from_md(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    md = MarkdownIt()
    tokens = md.parse(content)
    items = []

    for token in tokens:
        if token.type == "fence" and token.tag == "code":
            sleep_time = None
            # Extract sleep time from the info string
            match = re.search(r'sleep=(\d+)', token.info)
            if match:
                sleep_time = int(match.group(1))
            items.append((token.content.strip(), sleep_time))
        elif token.type == "inline":
            shortcut_match = re.match(r'\[(Ctrl\+\w)\]', token.content)
            if shortcut_match:
                items.append((shortcut_match.group(1), None))

    return items




# async def main(connection):
#     app = await iterm2.async_get_app(connection)
    
#     # Find or create the specific window, tab, and session
#     session = await find_or_create_session(app, window_index=0, tab_index=6)    
#     commands = extract_commands_from_md("ollama.md")
#     for item in commands:
#         if item in keyboard_shortcuts:
#             await session.async_send_text(keyboard_shortcuts[item])
#         else:
#             await simulated_typing(session, item)
#         await asyncio.sleep(1)

async def main(connection):
    app = await iterm2.async_get_app(connection)
    
    # Find or create the specific window, tab, and session
    session = await find_or_create_session(app, window_index=2, tab_index=0)
    
    commands = extract_commands_from_md("ollama.md")
    for item, sleep_time in commands:
        if item in keyboard_shortcuts:
            await session.async_send_text(keyboard_shortcuts[item])
        else:
            await simulated_typing(session, item)
        
        # Use the specified sleep time or a default value (e.g., 1 second)
        await asyncio.sleep(sleep_time or 1)


iterm2.run_until_complete(main)

