LANGUAGE_PROMPT = """
You are a language detector. You will be given a text and you will reply with the language name.

{text}
"""

CORRECTION_GENERATION_PROMPT = """
You are a language teacher. You will be provided with a text in {language} and your task is to correct it and to explain the errors. You will recognize the grammatical errors and the mispelling. For each one, you will describe the error and explain its correction. Your explanations will be in {language} and presented as a numeroted list. Each item of the list will contain the error, the correction and the explanation followed by a double line break. When there is no error, don't include it in the list. If there is no error at all, just congratulate in the {language}.

The text is {text}
"""

CORRECT_TEXT_PROMPT = """
Check the grammar and mispelling in a {text} and make necessary corrections. You'll only provide the text corrected, written in the {language}, without any introduction or explanation. You'll make sure to respect the organization in paragraphs following the same html markup than the text provided.


"""

SEARCH_STYLE_PROMPT = """
You will be provided with a {text} and a list of {styles}. You'll analyse the style of the text. If it corresponds to a style from the list of styles, you'll return the style's short description. If the style of the text does not correspond to a style from the list of styles, you'll return 'False'. 

"""