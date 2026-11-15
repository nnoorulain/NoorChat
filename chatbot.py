"""The chatbot's response dictionary and matching rules."""

import difflib
import re

RESPONSES = {
    "hi": "Hey! Ask me about NLP, Python, or how this chatbot works.",
    "hello": "Hello! What would you like to know?",
    "what's your name": "I'm NoorChat, a chatbot by Noorulain.",
    "how was your day": "It's been great! Thanks for asking.",
    "what is nlp": "NLP stands for Natural Language Processing. It helps computers work with human language.",
    "what is python": "Python is the programming language I use to find a reply to your message.",
    "how do you work": "I clean up your message, look for a known phrase, then try fuzzy matching if I can't find one.",
    "what is fuzzy matching": "Fuzzy matching looks for similar text. For example, I can match 'what is npl' to 'what is nlp'.",
    "what can you do": "I can answer a few questions about NLP and Python, explain my matching rules, and chat with you.",
    "help": "Try 'What is NLP?', 'How do you work?', or 'What’s your name?'",
    "thank you": "You're welcome!",
    "bye": "Goodbye! Send another message whenever you want to chat.",
}


def get_reply(message):
    """Return a reply and the name of the rule that produced it."""
    # Lowercase, standardize apostrophes, and tidy punctuation and whitespace.
    clean = message.lower().replace("’", "'")
    clean = re.sub(r"[^\w\s']", " ", clean)
    clean = " ".join(clean.split())

    if not clean:
        return {"reply": "Type a word or question to get started.", "method": "Fallback"}

    if clean in RESPONSES:
        return {"reply": RESPONSES[clean], "method": "Exact match"}

    # Spaces mark word boundaries, so "hi" doesn't trigger inside "this".
    for phrase in RESPONSES:
        if f" {phrase} " in f" {clean} ":
            return {"reply": RESPONSES[phrase], "method": "Phrase match"}

    # Avoid guessing short greetings and compare the entire cleaned message.
    questions = [phrase for phrase in RESPONSES if len(phrase.split()) >= 3]
    matches = difflib.get_close_matches(clean, questions, n=1, cutoff=0.8)
    if matches:
        return {"reply": RESPONSES[matches[0]], "method": "Fuzzy match"}

    return {
        "reply": "I didn't catch that. Try asking 'What is NLP?' or type 'help' for ideas.",
        "method": "Fallback",
    }
