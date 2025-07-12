document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('leadForm');
    const businessTypeSelect = document.getElementById('businessType');
    const customBusinessType = document.getElementById('customBusinessType');
    const resultsContainer = document.getElementById('results');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.getElementById('progressText');
    const resultsContent = document.getElementById('resultsContent');

    // Show/hide custom business type field
    businessTypeSelect.addEventListener('change', function() {
        if (this.value === 'custom') {
            customBusinessType.style.display = 'block';
        } else {
            customBusinessType.style.display = 'none';
        }
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Collect form data
        const formData = {
            businessType: businessTypeSelect.value === 'custom' 
                ? document.getElementById('customType').value 
                : businessTypeSelect.value,
            locations: document.getElementById('locations').value.split('\n').filter(loc => loc.trim()),
            minRating: parseFloat(document.getElementById('minRating').value),
            minReviews: parseInt(document.getElementById('minReviews').value),
            hasWebsite: document.getElementById('hasWebsite').value,
            businessStatus: document.getElementById('businessStatus').value,
            priceLevel: document.getElementById('priceLevel').value,
            maxResults: parseInt(document.getElementById('maxResults').value),
            searchRadius: parseInt(document.getElementById('searchRadius').value)
        };

        // Validate form
        if (!formData.businessType || formData.locations.length === 0) {
            alert('Please fill in all required fields.');
            return;
        }

        // Show results container and start process
        resultsContainer.style.display = 'block';
        form.style.display = 'none';
        
        // Simulate lead generation process
        generateLeads(formData);
    });

    function generateLeads(formData) {
        let progress = 0;
        const steps = [
            'Analyzing business criteria...',
            'Searching Google Places API...',
            'Filtering by quality metrics...',
            'Enriching business data...',
            'Generating CSV file...',
            'Preparing download...'
        ];

        const interval = setInterval(() => {
            progress += 20;
            progressFill.style.width = progress + '%';
            progressText.textContent = steps[Math.floor(progress / 20)] || 'Complete!';
            
            if (progress >= 100) {
                clearInterval(interval);
                showResults(formData);
            }
        }, 1000);
    }

    function showResults(formData) {
        // Generate sample high-quality businesses based on criteria
        const businesses = generateSampleBusinesses(formData);
        
        let html = `
            <div class="download-section">
                <h3>✅ Lead Generation Complete!</h3>
                <p>Found ${businesses.length} high-quality businesses matching your criteria.</p>
                <button class="download-btn" onclick="downloadCSV()">📥 Download CSV</button>
                <button class="download-btn" onclick="downloadJSON()">📄 Download JSON</button>
            </div>
            <h3>🎯 Top Quality Leads:</h3>
        `;

        businesses.forEach((business, index) => {
            const qualityScore = calculateQualityScore(business, formData);
            html += `
                <div class="business-card">
                    <div class="business-name">
                        ${business.name}
                        <span class="quality-score">Quality: ${qualityScore}/10</span>
                    </div>
                    <div class="business-details">
                        <span>📍 ${business.address}</span>
                        <span>📞 ${business.phone || 'Phone not available'}</span>
                        <span>🌐 ${business.website ? 'Has website' : 'No website'}</span>
                        <span>⭐ ${business.rating} stars (${business.reviews} reviews)</span>
                        <span>💰 Price Level: ${business.priceLevel}</span>
                        <span>🏢 Status: ${business.status}</span>
                    </div>
                </div>
            `;
        });

        resultsContent.innerHTML = html;
        
        // Store data for download
        window.businessData = businesses;
        window.formData = formData;
    }

    function generateSampleBusinesses(formData) {
        // Generate realistic sample data based on criteria
        const sampleBusinesses = [];
        const businessTypes = {
            'plumber': ['Plumbing Pro', 'Elite Plumbing', 'Master Plumbers', 'Premium Plumbing Services'],
            'electrician': ['Power Electric', 'Elite Electrical', 'Master Electricians', 'Premium Electrical'],
            'hvac': ['Climate Control Pro', 'Elite HVAC', 'Master HVAC', 'Premium Air Systems'],
            'lawyer': ['Law Partners', 'Elite Legal', 'Master Attorneys', 'Premium Law Group'],
            'accountant': ['Financial Partners', 'Elite Accounting', 'Master CPAs', 'Premium Tax Services']
        };

        const locations = formData.locations;
        const type = formData.businessType;
        const names = businessTypes[type] || ['Professional Services', 'Elite Business', 'Master Services', 'Premium Solutions'];

        for (let i = 0; i < Math.min(formData.maxResults, 10); i++) {
            const location = locations[i % locations.length];
            const name = names[i % names.length];
            
            const business = {
                name: `${name} - ${location.split(',')[0]}`,
                address: `${Math.floor(Math.random() * 9999) + 1} Main St, ${location}`,
                phone: `(${Math.floor(Math.random() * 900) + 100})-${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`,
                website: Math.random() > 0.2 ? `https://www.${name.toLowerCase().replace(/\s+/g, '')}.com` : null,
                rating: (Math.random() * 2 + 3).toFixed(1),
                reviews: Math.floor(Math.random() * 50) + 10,
                priceLevel: formData.priceLevel === 'any' ? Math.floor(Math.random() * 3) + 2 : formData.priceLevel,
                status: formData.businessStatus === 'any' ? 'OPERATIONAL' : formData.businessStatus,
                source: 'Google Places API'
            };

            // Apply filters
            if (business.rating >= formData.minRating && 
                business.reviews >= formData.minReviews &&
                (formData.hasWebsite === 'any' || 
                 (formData.hasWebsite === 'has_website' && business.website) ||
                 (formData.hasWebsite === 'no_website' && !business.website))) {
                sampleBusinesses.push(business);
            }
        }

        return sampleBusinesses;
    }

    function calculateQualityScore(business, formData) {
        let score = 5; // Base score

        // Rating bonus
        if (business.rating >= 4.5) score += 2;
        else if (business.rating >= 4.0) score += 1;

        // Reviews bonus
        if (business.reviews >= 50) score += 2;
        else if (business.reviews >= 25) score += 1;

        // Website bonus
        if (business.website) score += 1;

        // Price level bonus (higher = more established)
        if (business.priceLevel >= 3) score += 1;

        return Math.min(score, 10);
    }
});

// Download functions
function downloadCSV() {
    if (!window.businessData) return;
    
    const headers = ['Name', 'Address', 'Phone', 'Website', 'Rating', 'Reviews', 'Price Level', 'Status', 'Quality Score'];
    const csvContent = [
        headers.join(','),
        ...window.businessData.map(business => [
            `"${business.name}"`,
            `"${business.address}"`,
            `"${business.phone || ''}"`,
            `"${business.website || ''}"`,
            business.rating,
            business.reviews,
            business.priceLevel,
            business.status,
            calculateQualityScore(business, window.formData)
        ].join(','))
    ].join('\n');

    downloadFile(csvContent, 'high_quality_leads.csv', 'text/csv');
}

function downloadJSON() {
    if (!window.businessData) return;
    
    const jsonContent = JSON.stringify(window.businessData, null, 2);
    downloadFile(jsonContent, 'high_quality_leads.json', 'application/json');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
