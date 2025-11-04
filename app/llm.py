import os, re
from google import genai
from google.genai import types # Import the types module for configuration

def llm_suggest_command(description: str) -> str | None:
    # 1. Check for the new GEMINI_API_KEY environment variable
    os.environ["GEMINI_API_KEY"] = "AIzaSyA_4GMmtm8aH3t-bbVRdSlDHeUvP3ePjj8"
    if not os.getenv("GEMINI_API_KEY"):
        return f'echo "[AI preview] {description}"'

    try:
        # 2. Initialize the Gemini Client
        # The client automatically picks up the GEMINI_API_KEY from the environment.
        client = genai.Client()

        # Define the system instruction (the model's persona/rules)
        system_instruction = (
            "You are a shell command generator. Given a natural-language task, "
            "output exactly ONE safe POSIX shell command. "
            "No backticks, no explanations, no comments. "
            "Avoid destructive actions unless the intent is explicit; "
            "if destructive, prefix with 'echo ' to show intent."
        )

        # Define the user prompt
        prompt = f"Task: {description}\nCommand:"

        # 3. Use client.models.generate_content with the system instruction and prompt
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), # Use a Gemini model
            contents=[prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                # Set temperature to 0.0 for more deterministic, command-like output
                temperature=0.0
            )
        )

        # 4. Robustly extract text from the Gemini response
        # The text is in the 'text' attribute of the response object
        text = response.text or ""

        cmd = text.strip()
        # Strip fences / labels if a model adds them anyway
        cmd = re.sub(r"^`+|`+$", "", cmd)
        cmd = re.sub(r"(?i)^command:\s*", "", cmd).strip()
        # Only take the first line
        cmd = cmd.splitlines()[0].strip() if cmd else ""
        return cmd or None
    except Exception as e:
        print(f"LLM error: {e}")
        return None