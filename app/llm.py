import os, re
from google import genai
from google.genai import types 

def llm_suggest_command(description: str) -> str | None:
    if not os.getenv("GEMINI_API_KEY"):
        return f'echo "[AI preview] {description}"'

    try:
        client = genai.Client()
        system_instruction = (
            "You are a shell command generator. Given a natural-language task, "
            "output exactly ONE safe POSIX shell command. "
            "No backticks, no explanations, no comments. "
            "Avoid destructive actions unless the intent is explicit; "
            "if destructive, prefix with 'echo ' to show intent."
        )

        prompt = f"Task: {description}\nCommand:"

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=[prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0
            )
        )

        text = response.text or ""

        cmd = text.strip()
        cmd = re.sub(r"^`+|`+$", "", cmd)
        cmd = re.sub(r"(?i)^command:\s*", "", cmd).strip()
        cmd = cmd.splitlines()[0].strip() if cmd else ""
        return cmd or None
    except Exception as e:
        print(f"LLM error: {e}")
        return None