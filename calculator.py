import speech_recognition as sr
import nltk
import re

# Download punkt tokenizer if not already
nltk.download('punkt', quiet=True)

def parse_expression(text):
    text = text.lower()
    # Remove filler words
    text = text.replace("what is", "").replace("calculate", "").replace("please", "").strip()
    
    # Tokenize text
    tokens = nltk.word_tokenize(text)
    
    # Mapping words to math operators
    ops = {
        "plus": "+",
        "add": "+",
        "added": "+",
        "minus": "-",
        "subtract": "-",
        "subtracted": "-",
        "times": "*",
        "multiplied": "*",
        "multiply": "*",
        "divided": "/",
        "divide": "/",
        "over": "/",
        "by": "",  # ignore 'by' as it is part of phrase "divided by"
        "mod": "%",
        "modulus": "%"
    }
    
    # Extract numbers and operators into expression string
    expr_tokens = []
    for token in tokens:
        # Check if token is number
        if re.fullmatch(r'\d+(\.\d+)?', token):  # integer or decimal number
            expr_tokens.append(token)
        elif token in ops:
            expr_tokens.append(ops[token])
    
    expr = " ".join(expr_tokens)
    return expr

def calculate(expression):
    try:
        # Evaluate safely using eval on filtered expression (numbers and + - * / %)
        allowed_chars = "0123456789+-*/. %"
        if any(c not in allowed_chars for c in expression):
            return "Sorry, I can only calculate basic arithmetic."
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error in calculation: {e}"

def main():
    print("Voice-Controlled Calculator")
    print("Say a math expression like 'What is 42 divided by 6?'")
    print("Say 'quit' or 'exit' to stop.")
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    
    while True:
        print("\nListening...")
        with mic as source:
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            
            if text.lower() in ["quit", "exit"]:
                print("Exiting calculator. Goodbye!")
                break
            
            expr = parse_expression(text)
            if not expr.strip():
                print("Sorry, I didn't catch a valid expression.")
                continue
            
            result = calculate(expr)
            print(f"Result: {result}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()
