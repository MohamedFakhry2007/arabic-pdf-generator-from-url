document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('url-input');
    const convertBtn = document.getElementById('convert-btn');
    const errorMessage = document.getElementById('error-message');
    const resultContainer = document.getElementById('result-container');
    const downloadLink = document.getElementById('download-link');
    const loading = document.getElementById('loading');
    
    // Event listeners
    convertBtn.addEventListener('click', convertUrl);
    urlInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            convertUrl();
        }
    });
    
    /**
     * Converts the URL to PDF
     */
    async function convertUrl() {
        const url = urlInput.value.trim();
        
        // Clear previous errors and results
        errorMessage.textContent = '';
        resultContainer.classList.add('hidden');
        
        // Validate URL
        if (!url) {
            errorMessage.textContent = 'يرجى إدخال رابط صحيح';
            return;
        }
        
        // Show loading
        loading.classList.remove('hidden');
        
        try {
            // Send API request
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });
            
            const data = await response.json();
            
            // Hide loading
            loading.classList.add('hidden');
            
            if (data.success) {
                // Show success and download link
                resultContainer.classList.remove('hidden');
                downloadLink.href = data.pdf_path;
                // Focus on download button for accessibility
                downloadLink.focus();
            } else {
                // Show error message
                errorMessage.textContent = data.error || 'حدث خطأ أثناء تحويل الصفحة';
            }
            
        } catch (error) {
            // Hide loading and show error
            loading.classList.add('hidden');
            errorMessage.textContent = 'حدث خطأ في الاتصال. يرجى المحاولة مرة أخرى';
            console.error('Error converting URL:', error);
        }
    }
});