from flask import Blueprint, render_template, request, jsonify
import asyncio
from loguru import logger
from app.services.pdf_service import PDFService

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """Render the main page"""
    return render_template('index.html')

@main_bp.route('/convert', methods=['POST'])
async def convert_url():
    """
    API endpoint to convert URL to PDF
    
    Returns:
        JSON: Result of the conversion operation
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            logger.warning("No URL provided")
            return jsonify({'success': False, 'error': 'يرجى إدخال رابط صحيح'}), 400
            
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Convert URL to PDF
        result = await PDFService.convert_url_to_pdf(url)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'تم تحويل الصفحة إلى PDF بنجاح',
                'pdf_path': result['pdf_path']
            })
        else:
            error_message = result['error'] or 'حدث خطأ أثناء تحويل الصفحة'
            return jsonify({
                'success': False,
                'error': error_message
            }), 500
            
    except Exception as e:
        logger.error(f"Error in convert_url: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'حدث خطأ في الخادم. يرجى المحاولة مرة أخرى'
        }), 500