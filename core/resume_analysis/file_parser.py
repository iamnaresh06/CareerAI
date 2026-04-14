"""
File Parsing Utility for CareerAI.

This module provides functions to extract raw text content from common resume file formats
such as PDF and DOCX. It handles file reading and text sanitization.

Dependencies:
    - pdfplumber (for PDF extraction)
    - python-docx (for DOCX extraction)
    - re (Regular Expressions for text cleaning)

Author: Naresh Reddy
"""

import pdfplumber
import docx
import re
import os

def extract_text_from_pdf(file_path):
    """
    Opens a PDF file and extracts text from all pages.
    
    Args:
        file_path (str): The absolute path to the PDF file.
        
    Returns:
        str: The concatenated text content from the PDF, or empty string on failure.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        # In a real app, logging would happen here
        print(f"Error reading PDF {file_path}: {e}")
        return ""
        
    return text


def extract_text_from_docx(file_path):
    """
    Opens a DOCX file and extracts text from all paragraphs.
    
    Args:
        file_path (str): The absolute path to the DOCX file.
        
    Returns:
        str: The concatenated text content from the DOCX.
    """
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return " ".join(full_text)
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""


def clean_text(text):
    """
    Sanitizes raw text for NLP processing.
    
    - Removes excessive whitespace.
    - Removes special characters (keeping only alphanumeric, periods, spaces).
    
    Args:
        text (str): The raw input text.
        
    Returns:
        str: Cleaned, normalized text.
    """
    if not text:
        return ""
    
    # Replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove characters that aren't alphanumeric or common punctuation
    # Keeping only A-Z, a-z, 0-9, ., ,, and space
    text = re.sub(r'[^a-zA-Z0-9., ]', '', text)
    
    return text.strip()


def extract_resume_text(file_path):
    """
    Main entry point for extracting text from a resume file.
    Detects format based on extension.
    
    Args:
        file_path (str): The absolute path to the resume file.
        
    Returns:
        str: The extracted and cleaned text content.
    """
    if not os.path.exists(file_path):
        return ""

    _, ext = os.path.splitext(file_path)
    raw_text = ""

    if ext.lower() == '.pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif ext.lower() == '.docx':
        raw_text = extract_text_from_docx(file_path)
    else:
        # Unsupported format
        return ""

    return clean_text(raw_text)
