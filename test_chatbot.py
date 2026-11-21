import unittest

from chatbot import RESPONSES, get_reply


class ChatbotTests(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(get_reply("  WHAT IS NLP?  "), RESPONSES["what is nlp"])

    def test_phrase_match(self):
        self.assertEqual(
            get_reply("Please tell me what is NLP"),
            RESPONSES["what is nlp"],
        )

    def test_fuzzy_match(self):
        self.assertEqual(get_reply("What is npl?"), RESPONSES["what is nlp"])
