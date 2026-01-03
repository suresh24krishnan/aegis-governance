from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class AegisShield:
    def __init__(self):
        # The 'Brain' that finds sensitive info
        self.analyzer = AnalyzerEngine()
        # The 'Hand' that masks/scrubs it
        self.anonymizer = AnonymizerEngine()

    def protect_prompt(self, raw_prompt: str):
        """
        Analyzes a prompt and masks PII before it hits the LLM.
        """
        # 1. Identify PII (Names, Emails, Phone Numbers, etc.)
        results = self.analyzer.analyze(text=raw_prompt, language='en')

        # 2. Define how to mask (e.g., replace with [EMAIL_ADDRESS])
        # You can also use 'hash' or 'encrypt' here for more complexity!
        operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "[NAME]"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
            "PHONE_NUMBER": OperatorConfig("mask", {"chars_to_mask": 6, "masking_char": "*", "from_end": True}),
        }

        # 3. Perform the anonymization
        anonymized_result = self.anonymizer.anonymize(
            text=raw_prompt,
            analyzer_results=results,
            operators=operators
        )
        
        return anonymized_result.text

# --- Quick Test ---
if __name__ == "__main__":
    shield = AegisShield()
    sample_input = "Hi, my name is John Doe. My email is john.doe@example.com and phone is 555-0199."
    
    protected_text = shield.protect_prompt(sample_input)
    print(f"Original: {sample_input}")
    print(f"Protected: {protected_text}")