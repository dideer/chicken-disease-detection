/*
   ==================================================
   MAIN.JS - Shared Logic & Functions
   ==================================================
   
   This file contains:
   - Language switching functionality
   - Authentication guard
   - Dynamic element translation
   - Shared navigation logic
   ==================================================
*/

// ===== LANGUAGE SWITCHING =====

/**
 * Switch the application language
 * @param {string} lang - Language code ('en', 'rw', 'fr')
 */
function switchLanguage(lang) {
    // Validate language
    if (!translations[lang]) {
        console.warn('Invalid language:', lang);
        return;
    }
    
    // Save to localStorage
    setLanguage(lang);
    
    // Update all translatable elements
    loadLanguage();
}

/**
 * Load and apply the saved language to all elements
 */
function loadLanguage() {
    const currentLang = getCurrentLanguage();
    
    // Find all elements with data-lang-key attribute
    const elements = document.querySelectorAll('[data-lang-key]');
    
    elements.forEach(element => {
        updateLanguageForElement(element, currentLang);
    });
    
    // Update document language
    document.documentElement.lang = currentLang;
    
    // Update input placeholders if they have data-lang-key
    updatePlaceholders(currentLang);
}

/**
 * Update language for a specific element
 * @param {HTMLElement} element - The element to update
 * @param {string} lang - Language code (optional)
 */
function updateLanguageForElement(element, lang = null) {
    const currentLang = lang || getCurrentLanguage();
    const langKey = element.getAttribute('data-lang-key');
    
    if (!langKey) return;
    
    const translation = getTranslation(langKey, currentLang);
    
    // Update text content
    if (element.tagName === 'INPUT' && element.type === 'button') {
        element.value = translation;
    } else if (element.tagName === 'BUTTON') {
        // Preserve button content structure (icons, etc.)
        const hasIcon = element.querySelector('i');
        if (hasIcon) {
            element.innerHTML = hasIcon.outerHTML + ' ' + translation;
        } else {
            element.textContent = translation;
        }
    } else if (element.tagName === 'SPAN' || element.tagName === 'A') {
        element.textContent = translation;
    } else if (element.tagName === 'LABEL' || element.tagName === 'H1' || 
               element.tagName === 'H2' || element.tagName === 'H3' ||
               element.tagName === 'H4' || element.tagName === 'H5' ||
               element.tagName === 'H6' || element.tagName === 'P' ||
               element.tagName === 'DIV') {
        element.textContent = translation;
    } else {
        element.textContent = translation;
    }
}

/**
 * Update input placeholders based on language
 * @param {string} lang - Language code
 */
function updatePlaceholders(lang) {
    // Map input field data-lang-key to placeholder translations
    const placeholderMap = {
        'username': 'Username',
        'password': 'Password',
        'email': 'Email'
    };
    
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
    inputs.forEach(input => {
        const id = input.id;
        if (id.includes('username')) {
            input.placeholder = getTranslation('username', lang) || 'Username';
        } else if (id.includes('password')) {
            input.placeholder = getTranslation('password', lang) || 'Password';
        } else if (id.includes('email')) {
            input.placeholder = getTranslation('email', lang) || 'Email';
        }
    });
}

// ===== AUTHENTICATION =====

/**
 * Check if user is authenticated
 * Redirects to login if not authenticated
 * @param {function} callback - Function to execute if authenticated
 */
function checkAuth(callback = null) {
    const authToken = localStorage.getItem('authToken');
    
    if (!authToken) {
        // Redirect to login page
        window.location.href = 'login.html';
        return false;
    }
    
    // User is authenticated
    if (callback && typeof callback === 'function') {
        callback();
    }
    
    return true;
}

/**
 * Check if user is NOT authenticated
 * Redirects to dashboard if already logged in
 * @param {function} callback - Function to execute if not authenticated
 */
function checkAuthNot(callback = null) {
    const authToken = localStorage.getItem('authToken');
    
    if (authToken) {
        // User is already logged in, redirect to dashboard
        window.location.href = 'dashboard.html';
        return false;
    }
    
    // User is not authenticated
    if (callback && typeof callback === 'function') {
        callback();
    }
    
    return true;
}

/**
 * Get authorization headers for API requests
 * @returns {object} Headers object with auth token
 */
function getAuthHeaders() {
    const authToken = localStorage.getItem('authToken');
    
    return {
        'Content-Type': 'application/json',
        'Authorization': authToken ? `Bearer ${authToken}` : ''
    };
}

/**
 * Wrapper function for API requests with automatic auth token handling
 * Automatically adds auth headers, handles 401 Unauthorized responses,
 * and handles network errors gracefully
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options (method, body, etc.)
 * @returns {Promise<object>} Parsed JSON response
 * @throws {Error} On network error or non-200 responses
 */
async function apiFetch(url, options = {}) {
    try {
        // Merge auth headers into request headers
        const headers = {
            ...getAuthHeaders(),
            ...options.headers
        };
        
        const finalOptions = {
            ...options,
            headers
        };
        
        // Send request to backend
        const response = await fetch(url, finalOptions);
        
        // Parse response JSON
        const data = await response.json();
        
        // Handle 401 Unauthorized - token expired or invalid
        if (response.status === 401) {
            // Clear authentication data
            localStorage.removeItem('authToken');
            localStorage.removeItem('currentUser');
            localStorage.removeItem('loggedInUser');
            localStorage.removeItem('isAdmin');
            
            // Redirect to login page
            window.location.href = 'login.html';
            
            // Throw error to stop execution
            throw new Error('Session expired. Please login again.');
        }
        
        // Return response data (let caller handle success/failure based on 'success' field)
        return data;
        
    } catch (error) {
        // Handle network errors
        if (error.message.includes('Session expired')) {
            throw error;
        }
        
        console.error('API Request Error:', error);
        
        throw {
            message: 'Cannot connect to server. Please try again.',
            originalError: error
        };
    }
}

/**
 * Logout the current user
 * Clears authentication data and redirects to login page
 */
function logout() {
    // Clear authentication data from localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('loggedInUser');
    localStorage.removeItem('isAdmin');
    
    // Clear any app-specific data
    localStorage.removeItem('uploadedImage');
    localStorage.removeItem('detectionResult');
    
    // Redirect to login page
    window.location.href = 'login.html';
}

// ===== LOCAL STORAGE MANAGEMENT =====

/**
 * Save data to localStorage with error handling
 * @param {string} key - Storage key
 * @param {*} value - Value to store
 */
function saveToStorage(key, value) {
    try {
        if (typeof value === 'object') {
            localStorage.setItem(key, JSON.stringify(value));
        } else {
            localStorage.setItem(key, value);
        }
        return true;
    } catch (e) {
        console.error('Error saving to localStorage:', e);
        return false;
    }
}

/**
 * Retrieve data from localStorage with error handling
 * @param {string} key - Storage key
 * @param {boolean} parse - Should parse as JSON
 * @returns {*} Stored value or null
 */
function getFromStorage(key, parse = false) {
    try {
        const value = localStorage.getItem(key);
        if (parse && value) {
            return JSON.parse(value);
        }
        return value;
    } catch (e) {
        console.error('Error reading from localStorage:', e);
        return null;
    }
}

/**
 * Remove data from localStorage
 * @param {string} key - Storage key
 */
function removeFromStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (e) {
        console.error('Error removing from localStorage:', e);
        return false;
    }
}

/**
 * Clear all app data from localStorage
 */
function clearAppData() {
    try {
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
        localStorage.removeItem('loggedInUser');
        localStorage.removeItem('isAdmin');
        localStorage.removeItem('uploadedImage');
        localStorage.removeItem('detectionResult');
        return true;
    } catch (e) {
        console.error('Error clearing app data:', e);
        return false;
    }
}

// ===== UTILITIES =====

/**
 * Format file size in readable format
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Debounce function to limit function calls
 * @param {function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {function} Debounced function
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {number} Strength level (0-4)
 */
function validatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 6) strength++;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    return Math.min(strength, 4);
}

/**
 * Generate a random ID
 * @returns {string} Random ID
 */
function generateId() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

// ===== EVENT LISTENERS =====

/**
 * Initialize app on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Load language on page load
    loadLanguage();
    
    // Log app startup
    console.log('Chicken Disease Detection App Loaded');
    console.log('Current Language:', getCurrentLanguage());
    console.log('Auth Token:', localStorage.getItem('authToken') ? 'Present' : 'Not Set');
});

/**
 * Handle before unload (optional cleanup)
 */
window.addEventListener('beforeunload', function() {
    // Perform any cleanup if needed
    // E.g., save unsaved data, close connections, etc.
});

// ===== KEYBOARD SHORTCUTS =====

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Alt + L to switch language (cycle through)
        if (event.altKey && event.key === 'l') {
            const langs = ['en', 'rw', 'fr'];
            const currentLang = getCurrentLanguage();
            const currentIndex = langs.indexOf(currentLang);
            const nextIndex = (currentIndex + 1) % langs.length;
            switchLanguage(langs[nextIndex]);
        }
        
        // Alt + Q to logout (quick logout)
        if (event.altKey && event.key === 'q') {
            if (confirm('Are you sure you want to logout?')) {
                clearAppData();
                window.location.href = 'login.html';
            }
        }
    });
}

// Initialize keyboard shortcuts on load
document.addEventListener('DOMContentLoaded', initializeKeyboardShortcuts);

// ===== ACCESSIBILITY HELPERS =====

/**
 * Make elements more accessible
 */
function improveAccessibility() {
    // Add ARIA labels to buttons without text
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
        if (!btn.getAttribute('aria-label') && btn.textContent.trim() === '') {
            const icon = btn.querySelector('i');
            if (icon) {
                btn.setAttribute('aria-label', icon.className);
            }
        }
    });
    
    // Add role to interactive elements
    const dropdownTriggers = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    dropdownTriggers.forEach(el => {
        if (!el.getAttribute('role')) {
            el.setAttribute('role', 'button');
        }
    });
}

// Improve accessibility on page load
document.addEventListener('DOMContentLoaded', improveAccessibility);

// ===== ERROR HANDLING =====

/**
 * Global error handler
 */
window.addEventListener('error', function(event) {
    console.error('Global Error:', event.error);
    // You can send this to a logging service or display to user
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled Promise Rejection:', event.reason);
});

// ===== CONSOLE UTILITIES (for development) =====

/**
 * Log current app state
 */
function logAppState() {
    console.log('=== APP STATE ===');
    console.log('Language:', getCurrentLanguage());
    console.log('Auth Token:', localStorage.getItem('authToken') ? 'Present' : 'Not Set');
    console.log('Current User:', localStorage.getItem('currentUser') || 'None');
    console.log('Has Image:', !!localStorage.getItem('uploadedImage'));
    console.log('Detection Result:', getFromStorage('detectionResult', true));
}

/**
 * Clear all localStorage (development utility)
 */
function clearAllStorage() {
    if (confirm('Clear all localStorage? This will log you out.')) {
        localStorage.clear();
        location.reload();
    }
}

// Make logging functions available in console
window.logAppState = logAppState;
window.clearAllStorage = clearAllStorage;
window.switchLanguage = switchLanguage;
