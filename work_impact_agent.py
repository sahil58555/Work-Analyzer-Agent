import logging
import os
from pathlib import Path
from docx import Document
from constant import SYSTEM_PROMPT
from llm_client import ask_llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global cache to store read files
_files_cache = None
_cache_timestamp = None

def read_docx_files_from_work_doc(force_reload=False):
    """
    Reads all .docx files from the work_doc directory and returns a dictionary
    with filename as key and text content as value.
    Uses caching to avoid re-reading files unless force_reload=True or files have changed.
    """
    global _files_cache, _cache_timestamp
    
    work_doc_path = Path(__file__).parent / "work_doc"
    
    if not work_doc_path.exists():
        logger.error(f"work_doc directory not found at {work_doc_path}")
        return {}
    
    # Check if we need to reload files
    current_timestamp = work_doc_path.stat().st_mtime
    
    # Return cached data if available and not forced to reload and directory hasn't changed
    if (not force_reload and 
        _files_cache is not None and 
        _cache_timestamp is not None and 
        _cache_timestamp == current_timestamp):
        logger.info(f"Using cached data for {len(_files_cache)} files")
        return _files_cache
    
    # Read files fresh
    logger.info("Reading files from work_doc directory...")
    file_dict = {}
    
    try:
        # Get all .docx files in the work_doc directory
        docx_files = list(work_doc_path.glob("*.docx"))
        logger.info(f"Found {len(docx_files)} .docx files in work_doc directory")
        
        for file_path in docx_files:
            try:
                # Read the document
                doc = Document(file_path)
                
                # Extract all text from paragraphs
                text_content = []
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():  # Only add non-empty paragraphs
                        text_content.append(paragraph.text.strip())
                
                # Join all paragraphs with newlines
                full_text = "\n".join(text_content)
                
                # Use filename without extension as the key
                file_name = file_path.stem
                file_dict[file_name] = full_text
                
                logger.info(f"Successfully read {file_name}: {len(full_text)} characters")
                
            except Exception as e:
                logger.error(f"Error reading file {file_path.name}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error accessing work_doc directory: {e}")
        return {}
    
    # Update cache
    _files_cache = file_dict
    _cache_timestamp = current_timestamp
    logger.info(f"Cached {len(file_dict)} files")
    
    return file_dict

def clear_files_cache():
    """
    Clears the cached files data, forcing the next call to read_docx_files_from_work_doc 
    to read files fresh from disk.
    """
    global _files_cache, _cache_timestamp
    _files_cache = None
    _cache_timestamp = None
    logger.info("Files cache cleared")

def work_impact_agent(user_prompt: str = ""):
    try:
        # Read all docx files and create dictionary
        files_dict = read_docx_files_from_work_doc()
        
        if not files_dict:
            logger.warning("No files were read successfully")
            return None
        
        logger.info(f"Preparing to send {len(files_dict)} documents to LLM")
        
        # Prepare the documents content for the LLM
        documents_content = "\n\n" + "="*80 + "\n"
        documents_content += "WORK DOCUMENTS TO ANALYZE:\n"
        documents_content += "="*80 + "\n\n"
        
        for file_name, content in files_dict.items():
            documents_content += f"📄 **{file_name}**\n"
            documents_content += f"{'-'*50}\n"
            documents_content += f"{content}\n\n"
        
        # Create the full user prompt that includes both user question and documents
        full_user_prompt = ""
        if user_prompt:
            full_user_prompt += f"USER REQUEST: {user_prompt}\n\n"
        
        full_user_prompt += documents_content

        ask_llm_response = ask_llm(system_prompt=SYSTEM_PROMPT, user_prompt=full_user_prompt)
        logger.info("Received response from LLM")       
        return ask_llm_response
    except Exception as e:
        logger.error(f"Error occurred in work_impact_agent: {e}")
        return {}