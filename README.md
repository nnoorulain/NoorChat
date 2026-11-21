# NoorChat

Noorulain's Natural Language Processing class project. NoorChat runs locally in a browser using Python's standard library.

## Run the project

1. Extract the ZIP and open a terminal in the extracted `NoorChat` folder.
2. On Windows, run `py app.py`. On Ubuntu or macOS, run `python3 app.py`. Python 3 must be installed.
3. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser. Keep the terminal running while you chat.
4. Press **Ctrl+C** in the terminal to stop it.

Use the **Companion** switch in the side panel to hide or show the character. Move your mouse onto the picture to go to the next pose. Move it away and back to cycle through Portrait, Laptop, and Phone. On a touch screen, tap the picture. All three pictures work offline.

To try **Recent chats**, send a message, choose **New chat**, then send a different message. Both sessions appear in the sidebar under their first messages. Select a session to reopen it. The last two chats survive a refresh or app restart and expire 24 hours after their last message. The Python server clears expired chats the next time it reads or writes history.

## Files to explain

| File | What it does |
| --- | --- |
| `chatbot.py` | Holds the responses and decides which reply to send. Start here. |
| `app.py` | Serves the web page and handles the `/chat` and `/history` requests. |
| `history.py` | Reads and writes recent chats and applies the two-chat and 24-hour limits. |
| `chat_history.json` | Stores messages and replies locally. Python creates it when you send the first message. |
| `frontend/index.html` | Defines the chat panel, input, examples, and companion switch. |
| `frontend/style.css` | Styles the chat, history, and companion for desktop and small screens. |
| `frontend/chat.js` | Sends messages to Python, displays replies, and controls the companion and her poses. |
| `frontend/companion*.webp` | Contains the three illustrated companion poses. |

## Demo for your presentation

| Type this | Label | Why |
| --- | --- | --- |
| `  WHAT IS NLP?  ` | Exact match | Cleaning turns the input into `what is nlp`, a dictionary key. |
| `Please tell me what is NLP` | Phrase match | The message contains the known phrase `what is nlp`. |
| `What is npl?` | Fuzzy match | `difflib.get_close_matches()` picks the closest known question. |
| `Can you book a flight?` | Fallback | The bot has no suitable stored reply. |

Explain that the class terminal loop read messages with `input()` and showed replies with `print()`. Here, the form collects input, JavaScript sends it to Python, and the chat panel displays the reply. Walk through `get_reply()` in order. It cleans the text, checks for an exact dictionary key, checks for a whole phrase, then tries one close match. The fuzzy cutoff of `0.8` requires a high similarity score. These rules depend on text similarity and known phrases, so a paraphrase can still fall through to the default reply.

To add a new answer, add one lowercase key and its reply to `RESPONSES` in `chatbot.py`. Restart `app.py` to see the change.

To explain the companion, show how `updateCompanion()` sets the panel's `hidden` property. Then show how `nextCompanionFrame()` advances through the image array when the mouse enters the picture. The remainder operator `%` takes the index back to zero after the last pose.

This project uses Jenkins for continuous integration.
Jenkins runs three chatbot reply tests.
