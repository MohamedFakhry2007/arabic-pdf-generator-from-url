import asyncio
import aiohttp
import os
import uuid
from datetime import datetime
from loguru import logger
from app.config import Config
import urllib.parse

class PDFService:
    """Service for converting URLs to PDFs using pdflayer API"""
    
    @staticmethod
    async def generate_unique_filename():
        """
        Generates a unique filename using the current timestamp and a UUID.
        
        Returns:
            str: A unique filename for the PDF
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        return f'pdf_{timestamp}_{unique_id}.pdf'
    
    @staticmethod
    async def convert_url_to_pdf(url: str, language: str = 'ar'):
        """
        Asynchronously converts the given URL to a PDF using the pdflayer API.
        
        Parameters:
            url (str): The URL of the webpage to convert
            language (str): The preferred language for the Accept-Language header
            
        Returns:
            dict: A dictionary containing the result of the operation
                {
                    'success': bool,
                    'filename': str or None,
                    'error': str or None,
                    'pdf_path': str or None
                }
        """
        logger.info(f"Starting PDF conversion for URL: {url}")
        
        try:
            # Generate a unique filename for the PDF
            filename = await PDFService.generate_unique_filename()
            logger.debug(f"Generated unique filename: {filename}")
            
            # Full path where the PDF will be saved
            pdf_path = os.path.join(Config.PDF_STORAGE_PATH, filename)
            relative_path = f"/static/pdfs/{filename}"
            
            # Prepare the parameters for the API request
            encoded_url = urllib.parse.quote_plus(url)
            params = {
                'access_key': Config.PDFLAYER_API_KEY,
                'document_url': encoded_url,
                'document_name': filename,
                'accept_lang': language,
                'text_encoding': 'utf-8',
                'inline': 0,
                'test': 1  # Set to 0 in production
            }
            
            async with aiohttp.ClientSession() as session:
                logger.info(f"Sending request to pdflayer API...")
                async with session.get(Config.PDFLAYER_API_ENDPOINT, params=params, timeout=30) as response:
                    logger.info(f"pdflayer API Response Status: {response.status}")
                    response_content = await response.read()
                    logger.info(f"pdflayer API Response Content: {response_content}")

                    if response.status != 200:
                        error_info = await response.json()
                        error = error_info.get('error', {})
                        error_msg = f"API Error {error.get('code')}: {error.get('info')}"
                        logger.error(error_msg)
                        return {'success': False, 'filename': None, 'error': error_msg, 'pdf_path': None}
                    
                    # Save the PDF content to a file
                    content = await response.read()
                    with open(pdf_path, 'wb') as f:
                        f.write(content)
                    
                    logger.success(f"PDF saved as: {pdf_path}")
                    return {
                        'success': True, 
                        'filename': filename, 
                        'error': None,
                        'pdf_path': relative_path
                    }
                    
        except aiohttp.ClientError as e:
            error_msg = f"HTTP Error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'filename': None, 'error': error_msg, 'pdf_path': None}
        except asyncio.TimeoutError:
            error_msg = "Request timed out"
            logger.error(error_msg)
            return {'success': False, 'filename': None, 'error': error_msg, 'pdf_path': None}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'filename': None, 'error': error_msg, 'pdf_path': None}