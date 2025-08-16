import os
import logging

# Initialize Gemini model with error handling
gemini_model = None

try:
    from vertexai import init
    from vertexai.language_models import TextGenerationModel
    
    # Initialize Vertex AI
    gcp_project = os.getenv("GCP_PROJECT")
    if gcp_project:
        init(project=gcp_project, location="us-central1")
        gemini_model = TextGenerationModel.from_pretrained("gemini-2.5-pro")
        logging.info("✅ Gemini model loaded successfully")
    else:
        logging.warning("⚠️ GCP_PROJECT not set, Gemini model unavailable")
        
except Exception as e:
    logging.warning(f"⚠️ Failed to initialize Gemini model: {e}")
    logging.warning("Gemini functionality will be disabled. Set up Google Cloud authentication to enable it.")

def generate_text(prompt: str, max_output_tokens: int = 512):
    """Generate text using Gemini model or return a mock response if unavailable"""
    if gemini_model is None:
        # Return a mock response when Gemini is unavailable
        return f"[MOCK RESPONSE] Generated text for prompt: {prompt[:50]}..."
    
    try:
        response = gemini_model.predict(prompt, max_output_tokens=max_output_tokens)
        return response.text
    except Exception as e:
        logging.error(f"Error generating text with Gemini: {e}")
        return f"[ERROR] Failed to generate text: {str(e)}"
