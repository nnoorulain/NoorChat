import unittest

from chatbot import RESPONSES, get_reply


class ChatbotTests(unittest.TestCase):
    def test_exact_match(self):
        result = get_reply("  WHAT IS NLP?  ")
        self.assertEqual(result["reply"], RESPONSES["what is nlp"])

    def test_phrase_match(self):
        result = get_reply("Please tell me what is NLP")
        self.assertEqual(result["reply"], RESPONSES["what is nlp"])

    def test_fuzzy_match(self):
        result = get_reply("What is npl?")
        self.assertEqual(result["reply"], RESPONSES["what is nlp"])
