import re
import logging

logger = logging.getLogger("janai")

class LanguageManager:
    """
    Production Object-Oriented Language Detection & Switching Service.
    Evaluates script character density and catches explicit mid-call switch phrases.
    """

    ENGLISH_SWITCH_PHRASES = [
        "in english", "english please", "speak english", "speak in english",
        "talk in english", "explain in english", "can you speak english",
        "tell me in english", "change to english", "switch to english",
        "english mein", "english me", "इंग्लिश में", "इंग्लिश", "एक्सप्लेन",
        "इन इंग्लिश"
    ]

    HINDI_SWITCH_PHRASES = [
        "hindi please", "speak hindi", "talk in hindi", "explain in hindi",
        "hindi mein", "hindi me", "हिंदी में", "हिंदी", "हिंदी प्लीज"
    ]

    @classmethod
    def detect_language_from_speech(cls, text: str, current_lang: str = "hi") -> str:
        """
        Detects language from transcribed speech text with priority for explicit switch phrases.
        """
        if not text:
            return current_lang

        clean_lower = text.lower().strip()

        # Check explicit English switch phrases
        for phrase in cls.ENGLISH_SWITCH_PHRASES:
            if phrase in clean_lower:
                logger.info(f"Language Switch: EXPLICIT ENGLISH phrase detected ('{phrase}') -> switching to 'en'")
                return "en"

        # Check explicit Hindi switch phrases
        for phrase in cls.HINDI_SWITCH_PHRASES:
            if phrase in clean_lower:
                logger.info(f"Language Switch: EXPLICIT HINDI phrase detected ('{phrase}') -> switching to 'hi'")
                return "hi"

        # Character script density evaluation
        devanagari_count = len(re.findall(r"[\u0900-\u097F]", text))
        latin_count = len(re.findall(r"[a-zA-Z]", text))
        total_letters = devanagari_count + latin_count

        if total_letters == 0:
            return current_lang

        # Ratio calculation
        devanagari_ratio = devanagari_count / total_letters
        if devanagari_ratio > 0.6:
            return "hi"
        elif devanagari_ratio < 0.3:
            return "en"

        return current_lang
