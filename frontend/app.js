const API_BASE_URL = 'http://localhost:8000'
let authToken = null;

// DOM Elements
const authButtons = document.getElementById('auth-buttons');
const userInfo = document.getElementById('user-info');
const usernameDisplay = document.getElementById('username-display');
const balanceDisplay = document.getElementById('balance-display');
const authForms = document.getElementById('auth-forms');
const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const predictionSection = document.getElementById('prediction-section');
const resultsSection = document.getElementById('results-section');
const historySection = document.getElementById('history-section');

// Show/hide auth forms
function showAuthForm(formType) {
    authForms.style.display = 'block';
    registerForm.style.display = formType === 'register' ? 'block' : 'none';
    loginForm.style.display = formType === 'login' ? 'block' : 'none';
}

function hideAuthForms() {
    document.getElementById('auth-forms').style.display = 'none';
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'none';
}

// Register user
async function register(event) {
    event.preventDefault();
    
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                email,
                password
            }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }
        
        const user = await response.json();
        alert('Registration successful! Please login.');
        showAuthForm('login');
        
        // Clear form
        document.getElementById('reg-username').value = '';
        document.getElementById('reg-email').value = '';
        document.getElementById('reg-password').value = '';
        
    } catch (error) {
        alert(error.message);
    }
}

async function login(event) {
    event.preventDefault();
    
    // Get form elements
    const emailInput = document.getElementById('login-email');
    const passwordInput = document.getElementById('login-password');
    const loginButton = event.target.querySelector('button[type="submit"]');
    
    // Store original button text
    const originalButtonText = loginButton.textContent;
    
    try {
        // Show loading state
        loginButton.disabled = true;
        loginButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...';
        
        // Perform login request
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                email: emailInput.value.trim(),
                password: passwordInput.value
            })
        });

        // Handle response
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Login failed. Please try again.');
        }

        const { token } = await response.json();
        
        // Store token securely
        authToken = token;
        localStorage.setItem('authToken', token);
        
        // Update UI
        authButtons.style.display = 'none';
        userInfo.style.display = 'flex';
        hideAuthForms();
        
        // Load user data and show app interface
        await loadUserData();
        showAppInterface();
        
        // Clear password field
        passwordInput.value = '';
        
    } catch (error) {
        console.error('Login error:', error);
        
        // Show error to user
        const errorElement = document.getElementById('login-error');
        if (errorElement) {
            errorElement.textContent = error.message;
            errorElement.style.display = 'block';
        } else {
            alert(error.message);
        }
        
        // Reset password field on error
        passwordInput.value = '';
        passwordInput.focus();
        
    } finally {
        // Reset button state
        loginButton.disabled = false;
        loginButton.textContent = originalButtonText;
    }
}

// Helper function to show app interface
function showAppInterface() {
    document.getElementById('prediction-section').style.display = 'block';
    document.getElementById('history-section').style.display = 'block';
    document.getElementById('results-section').style.display = 'none';
    loadHistory();
}

// Helper function to hide auth forms
function hideAuthForms() {
    document.getElementById('auth-forms').style.display = 'none';
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'none';
    
    // Clear any error messages
    const errorElement = document.getElementById('login-error');
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

// Logout user
function logout() {
    authToken = null;
    localStorage.removeItem('authToken');
    userInfo.style.display = 'none';
    authButtons.style.display = 'block';
    predictionSection.style.display = 'none';
    resultsSection.style.display = 'none';
    historySection.style.display = 'none';
    
    // Clear forms
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
}

// Load user data
async function loadUserData() {
    try {
        const response = await fetch(`${API_BASE_URL}/user`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`,
            },
        });
        
        if (!response.ok) {
            throw new Error('Failed to load user data');
        }
        
        const user = await response.json();
        usernameDisplay.textContent = user.username;
        balanceDisplay.textContent = `${user.balance} credits`;
        
    } catch (error) {
        console.error('Error loading user data:', error);
        logout();  // Force logout if user data can't be loaded
    }
}

// Add money to user account
async function addMoney() {
    try {
        const response = await fetch(`${API_BASE_URL}/add_money`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json',
            },
            // Add empty body if your endpoint expects JSON
            body: JSON.stringify({}),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to add money');
        }
        
        const result = await response.json();
        balanceDisplay.textContent = `${result.new_balance} credits`;
        alert('Added 50 credits to your account!');
        
    } catch (error) {
        console.error('Add money error:', error);
        alert(error.message);
    }
}

// Make prediction
async function makePrediction(event) {
    event.preventDefault();
    
    const modelType = document.getElementById('model-type').value;
    const inputData = document.getElementById('input-data').value;
    
    try {
        const parsedInput = JSON.parse(inputData);
        
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
            },
            body: JSON.stringify({
                model_type: modelType,
                input_data: parsedInput
            }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Prediction failed');
        }
        
        const result = await response.json();
        
        // Show results
        resultsSection.style.display = 'block';
        document.getElementById('prediction-result').textContent = JSON.stringify(result.result, null, 2);
        document.getElementById('cost-display').textContent = `Cost: ${result.cost} credits`;
        document.getElementById('balance-after').textContent = `Remaining balance: ${result.remaining_balance} credits`;
        
        // Update balance display
        balanceDisplay.textContent = `${result.remaining_balance} credits`;
        
        // Reload history
        await loadHistory();
        
    } catch (error) {
        if (error instanceof SyntaxError) {
            alert('Invalid JSON input');
        } else {
            alert(error.message);
        }
    }
}

// Load prediction history
async function loadHistory() {
    console.log("Loading history...");
    console.log("Current auth token:", authToken);  // Verify token exists
    
    try {
        const response = await fetch(`${API_BASE_URL}/predictions_history`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            credentials: 'include'  // Important for cookie-based auth
        });

        console.log("Response status:", response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error("Error details:", errorData);
            
            // Handle token expiration
            if (response.status === 401) {
                logout();
                throw new Error("Session expired. Please login again.");
            }
            
            throw new Error(errorData.detail || "Failed to load history");
        }

        const data = await response.json();
        console.log("History data:", data);
        renderHistory(data.predictions || []);
        
    } catch (error) {
        console.error("History load failed:", error);
        showErrorToast(`Failed to load history: ${error.message}`);
    }
}

function renderHistory(predictions) {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';

    if (!predictions || predictions.length === 0) {
        historyList.innerHTML = `
            <div class="text-muted text-center py-3">
                No predictions made yet
            </div>
        `;
        return;
    }

    predictions.forEach(prediction => {
        const date = new Date(prediction.created_at);
        const formattedDate = date.toLocaleString();
        
        const item = document.createElement('div');
        item.className = 'list-group-item history-item mb-2';
        item.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
                <div class="me-3">
                    <div class="d-flex align-items-center mb-1">
                        <strong class="me-2">${prediction.model_type}</strong>
                        <span class="badge bg-${getModelBadgeColor(prediction.model_type)}">
                            ${prediction.cost} credits
                        </span>
                    </div>
                    <small class="text-muted">${formattedDate}</small>
                </div>
                <button class="btn btn-sm btn-outline-secondary toggle-details">
                    Details
                </button>
            </div>
            <div class="prediction-details mt-2" style="display: none;">
                <div class="card card-body bg-light">
                    <div class="mb-2">
                        <strong>Input:</strong>
                        <pre class="mb-0 mt-1 p-2 bg-white rounded">${JSON.stringify(prediction.input_data, null, 2)}</pre>
                    </div>
                    <div>
                        <strong>Output:</strong>
                        <pre class="mb-0 mt-1 p-2 bg-white rounded">${JSON.stringify(prediction.output_data, null, 2)}</pre>
                    </div>
                </div>
            </div>
        `;

        // Add click handler for toggling details
        const toggleBtn = item.querySelector('.toggle-details');
        const detailsDiv = item.querySelector('.prediction-details');
        
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const isShowing = detailsDiv.style.display === 'block';
            detailsDiv.style.display = isShowing ? 'none' : 'block';
            toggleBtn.textContent = isShowing ? 'Details' : 'Hide';
        });

        historyList.appendChild(item);
    });
}

// Helper function for model type badge colors
function getModelBadgeColor(modelType) {
    const colors = {
        'cheap': 'warning',
        'medium': 'info',
        'expensive': 'success'
    };
    return colors[modelType] || 'primary';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const savedToken = localStorage.getItem('authToken');
    if (savedToken) {
        authToken = savedToken;
        checkAuthStatus();
    }
});

async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/user`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            usernameDisplay.textContent = user.username;
            balanceDisplay.textContent = `${user.balance} credits`;
            authButtons.style.display = 'none';
            userInfo.style.display = 'block';
            showAppInterface();
        } else {
            logout();
        }
    } catch (error) {
        logout();
    }
}

function initializeEventListeners() {
    // Handle refresh button (with event delegation)
    document.body.addEventListener('click', (event) => {
        if (event.target.closest('#refresh-button')) {
            event.preventDefault();
            loadHistory();
        }
    });
}

// Modified loadHistory function
async function loadHistory() {
    if (!authToken) {
        console.error("Cannot refresh: No authentication token");
        showToast("Please login first", "error");
        return;
    }

    const refreshBtn = document.getElementById('refresh-button');
    if (refreshBtn) {
        refreshBtn.disabled = true;
        refreshBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Loading...';
    }

    try {
        console.debug("Attempting to refresh history...");
        const response = await fetch(`${API_BASE_URL}/predictions_history`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        renderHistory(data.predictions || []);
        
    } catch (error) {
        console.error("Refresh failed:", error);
        showToast("Failed to refresh history", "error");
    } finally {
        if (refreshBtn) {
            refreshBtn.disabled = false;
            refreshBtn.textContent = 'Refresh';
        }
    }
}

function showToast(message, type = 'info') {
    const toastEl = document.getElementById('liveToast');
    const toastBody = toastEl.querySelector('.toast-body');
    
    // Remove previous type classes
    toastEl.classList.remove('text-bg-primary', 'text-bg-success', 'text-bg-danger', 'text-bg-warning');
    
    // Add type-specific styling
    const typeClasses = {
      success: 'text-bg-success',
      error: 'text-bg-danger',
      warning: 'text-bg-warning',
      info: 'text-bg-primary'
    };
    toastEl.classList.add(typeClasses[type] || 'text-bg-primary');
  
    toastBody.textContent = message;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }

// Call this when your app initializes
document.addEventListener('DOMContentLoaded', initializeEventListeners);