import google.generativeai as genai
import json
import logging
import asyncio
from app.config import settings
from google.api_core import exceptions as google_exceptions

class GeminiService:
    def __init__(self):
        self.model = None
        self.embedding_model = None
        
        if not settings.GEMINI_API_KEY:
            logging.error("❌ ERROR: GEMINI_API_KEY is missing in .env file.")
            return

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Try to initialize the configured model
            try:
                self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
                logging.info(f"✅ Gemini Service Initialized with model: {settings.GEMINI_MODEL}")
            except google_exceptions.NotFound:
                logging.error(f"❌ Model '{settings.GEMINI_MODEL}' not found.")
                self._list_available_models()
                return

            self.embedding_model = 'models/text-embedding-004'

        except Exception as e:
            logging.error(f"❌ Failed to configure Gemini: {e}")

    def _list_available_models(self):
        """Helper to print models the user ACTUALLY has access to."""
        try:
            logging.info("🔍 Attempting to list available models for your API key...")
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            logging.warning(f"⚠️ YOUR AVAILABLE MODELS: {available_models}")
            logging.warning("👉 Please update GEMINI_MODEL in your .env file to one of the models listed above (e.g., 'gemini-flash-latest').")
        except Exception as e:
            logging.error(f"Could not list models: {e}")

    async def _generate_with_retry(self, prompt, retries=3, delay=5):
        """Helper to handle 429 Rate Limit errors automatically."""
        for attempt in range(retries):
            try:
                return await self.model.generate_content_async(prompt)
            except Exception as e:
                error_msg = str(e)
                # Check for Rate Limit (429) or Quota errors
                if "429" in error_msg or "quota" in error_msg.lower():
                    if attempt < retries - 1:
                        logging.warning(f"⚠️ Rate limit hit. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                        await asyncio.sleep(delay)
                        delay *= 2  # Exponential backoff (wait longer each time)
                        continue
                raise e

    async def parse_task_intent(self, user_task: str) -> dict:
        """
        Uses LLM to understand what the user wants to do and maps it to a tool.
        """
        if not self.model:
            raise ValueError("Gemini Model is not active. Check terminal logs.")

        prompt = f"""
        You are an intelligent automation agent. Map the following user task to one of the defined tools.
        
        USER TASK: "{user_task}"

        AVAILABLE TOOLS:
        1. install_uv_datagen: Install 'uv' and run 'datagen.py'. (args: user_email)
        2. format_markdown: Format a markdown file using prettier. (args: file_path)
        3. count_weekdays: Count specific weekdays in a file. (args: file_path, target_weekday_name, output_file)
        4. sort_json: Sort a JSON array by keys. (args: file_path, sort_keys: list[str], output_file)
        5. extract_recent_logs: specific task to extract first lines of recent log files. (args: logs_dir, output_file, count: int)
        6. create_index: Create an index of H1 titles from Markdown files. (args: docs_dir, output_file)
        7. extract_email_sender: Extract sender email address. (args: file_path, output_file)
        8. extract_credit_card: Extract credit card number from image. (args: image_path, output_file)
        9. find_similar_comments: Find similar comments using embeddings. (args: file_path, output_file)
        10. query_database: Run SQL query on SQLite/DuckDB. (args: db_path, query, output_file)
        
        Return ONLY a JSON object. Do not include markdown formatting.
        Example:
        {{ "tool": "sort_json", "args": {{ "file_path": "/data/contacts.json", "sort_keys": ["last_name", "first_name"], "output_file": "/data/contacts-sorted.json" }} }}
        """
        
        try:
            # USE THE RETRY HELPER HERE
            response = await self._generate_with_retry(prompt)
            
            clean_text = response.text.strip()
            if clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1]
                if clean_text.startswith("json"):
                    clean_text = clean_text[4:]
            clean_text = clean_text.strip()
            
            logging.info(f"LLM Response: {clean_text}")
            return json.loads(clean_text)
            
        except Exception as e:
            logging.error(f"❌ LLM Error: {e}")
            raise ValueError(f"Gemini API Error: {str(e)}")

    async def get_image_content(self, image_data: bytes, prompt: str):
        if not self.model:
            raise ValueError("Gemini Model is not active.")
        
        # We can implement retry logic here too if needed, but manual implementation for lists is tricky
        # For now, let's wrap the call directly
        try:
             response = await self.model.generate_content_async([
                {'mime_type': 'image/png', 'data': image_data},
                prompt
            ])
             return response.text.strip()
        except Exception as e:
             if "429" in str(e):
                 # Simple one-time retry for images
                 logging.warning("⚠️ Rate limit on image. Waiting 5s...")
                 await asyncio.sleep(5)
                 response = await self.model.generate_content_async([
                    {'mime_type': 'image/png', 'data': image_data},
                    prompt
                ])
                 return response.text.strip()
             raise e

    async def get_embedding(self, text: str):
        if not self.model:
            raise ValueError("Gemini Model is not active.")
        
        # Embeddings have their own limits, usually higher, but good to be safe
        result = await genai.embed_content_async(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

llm_client = GeminiService()