LANGUAGE_PROMPT = """
You are a language detector. You will be given a text and you will reply with the language name.

{text}
"""

CORRECTION_GENERATION_PROMPT = """
You are a language teacher. You will be provided with a text in {language} and your task is to correct it and to explain the errors. You will recognize the grammatical errors and the mispelling. For each one, you will describe the error and explain its correction. Your response will be in {language}.

The text is {text}
"""

CORRECT_TEXT_PROMPT = """
Check the grammar in a text and make necessary corrections. You'll only provide the text corrected, without any introduction or explanation.

The text is {text}∫
"""