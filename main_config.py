import os

CONFIGS = {
    "api": os.getenv("GEMINI_API_KEY"),
    "template_prompt": "You are a expert on anything in and about the game Subnautica and subnautica below zero. Answer all question with total accuratcy."
}