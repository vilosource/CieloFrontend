# CieloFrontend Authentication Integration Guide

This document provides comprehensive guidance for implementing and maintaining authentication features in the CieloFrontend Django project.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Frontend Implementation](#frontend-implementation)
- [Session Management](#session-management)
- [JavaScript API Integration](#javascript-api-integration)
- [Template Integration](#template-integration)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)
- [Testing Authentication](#testing-authentication)
- [Troubleshooting](#troubleshooting)

## Overview

CieloFrontend is a presentation-layer Django application that handles user interface rendering while delegating all authentication logic to the CieloIdentityProvider service. This separation of concerns ensures:

- **Clean Architecture**: UI and authentication logic are separated
- **Scalability**: Frontend can be replicated without authentication state
- **Security**: Credentials are only handled by the dedicated identity service
- **Flexibility**: Frontend remains agnostic to authentication implementation

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Browser     │    │  CieloFrontend  │    │CieloIdentityProv│
│                 │    │   (UI Layer)    │    │ider (Auth Layer)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │ 1. Request page       │                       │
         ├──────────────────────▶│                       │
         │                       │                       │
         │ 2. Serve HTML+JS      │                       │
         │◀──────────────────────┤                       │
         │                       │                       │
         │ 3. AJAX Auth Request  │                       │
         ├──────────────────────────────────────────────▶│
         │                       │                       │
         │ 4. Auth Response      │                       │
         │◀──────────────────────────────────────────────┤
         │                       │                       │
         │ 5. Update UI          │                       │
         │◀──────────────────────┤                       │
```

### Key Principles

1. **Frontend serves static content** (HTML, CSS, JavaScript)
2. **JavaScript makes AJAX calls** to identity provider
3. **Sessions are shared** via `.cielo.test` domain cookies
4. **No authentication logic** in frontend Django code
5. **Graceful fallbacks** for authentication failures

## Frontend Implementation

### Django Settings Configuration

```python
# In cielo_frontend/settings/dev.py

# Session configuration to work with Identity Provider
SESSION_COOKIE_DOMAIN = ".cielo.test"
SESSION_COOKIE_NAME = 'cielo_sessionid'
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False  # Development only
SESSION_COOKIE_HTTPONLY = False  # Allow JS access for debugging

# CORS settings for cross-origin requests
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://identity.cielo.test",
    "http://localhost:8002",
]

# Authentication backend (optional, for admin access)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

### URL Configuration

```python
# In cielo_frontend/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('users/', include('users.urls')),
]
```

### Views Implementation

```python
# In cielo_frontend/views.py
from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = 'index.html'

class LoginView(TemplateView):
    template_name = 'users/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login - Cielo'
        return context

class LogoutView(TemplateView):
    template_name = 'users/logout.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard - Cielo'
        # Note: User authentication is handled by JavaScript
        return context
```

## Session Management

### Cookie Handling

The frontend relies on the shared session cookie set by the Identity Provider:

```javascript
// Session cookie is automatically included in requests to *.cielo.test domains
// No manual cookie handling required in most cases

// For debugging, you can check if session cookie exists:
function hasSessionCookie() {
    return document.cookie.split(';').some(cookie => 
        cookie.trim().startsWith('cielo_sessionid=')
    );
}
```

### Session Validation Flow

1. **Page Load**: JavaScript checks session status
2. **Valid Session**: Continue with page functionality
3. **Invalid Session**: Redirect to login page
4. **No Session**: Show login form

## JavaScript API Integration

### Authentication Service Module

Create a reusable authentication service:

```javascript
// static/js/auth-service.js
class AuthService {
    constructor() {
        this.baseUrl = 'http://identity.cielo.test';
        this.endpoints = {
            login: '/login/',
            logout: '/logout/',
            checkSession: '/check-session/',
            currentUser: '/current-user/'
        };
    }

    async makeRequest(endpoint, options = {}) {
        const url = this.baseUrl + endpoint;
        const defaultOptions = {
            credentials: 'include', // Always include cookies
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const requestOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, requestOptions);
            return {
                ok: response.ok,
                status: response.status,
                data: response.ok ? await response.json() : null,
                error: !response.ok ? await response.text() : null
            };
        } catch (error) {
            console.error('Auth request failed:', error);
            return {
                ok: false,
                status: 0,
                data: null,
                error: error.message
            };
        }
    }

    async login(username, password) {
        return await this.makeRequest(this.endpoints.login, {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    }

    async logout() {
        return await this.makeRequest(this.endpoints.logout, {
            method: 'POST'
        });
    }

    async checkSession() {
        return await this.makeRequest(this.endpoints.checkSession);
    }

    async getCurrentUser() {
        return await this.makeRequest(this.endpoints.currentUser);
    }
}

// Global instance
window.authService = new AuthService();
```

### Login Form Handler

```javascript
// static/js/login.js
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const errorContainer = document.getElementById('login-error');
    const submitButton = document.getElementById('login-submit');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(loginForm);
            const username = formData.get('username');
            const password = formData.get('password');

            // Disable submit button
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';

            try {
                const result = await window.authService.login(username, password);
                
                if (result.ok) {
                    // Success - redirect to dashboard or intended page
                    const redirectUrl = new URLSearchParams(window.location.search).get('next') || '/dashboard/';
                    window.location.href = redirectUrl;
                } else {
                    // Show error
                    showError(result.error || 'Login failed. Please try again.');
                }
            } catch (error) {
                showError('Network error. Please check your connection.');
            } finally {
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.textContent = 'Login';
            }
        });
    }

    function showError(message) {
        if (errorContainer) {
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
        }
    }
});
```

### Session Validation

```javascript
// static/js/session.js
class SessionManager {
    constructor() {
        this.authService = window.authService;
        this.currentUser = null;
    }

    async validateSession() {
        try {
            const result = await this.authService.checkSession();
            
            if (result.ok && result.data.authenticated) {
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error('Session validation failed:', error);
            return false;
        }
    }

    async loadCurrentUser() {
        try {
            const result = await this.authService.getCurrentUser();
            
            if (result.ok) {
                this.currentUser = result.data;
                this.updateUserInterface();
                return this.currentUser;
            } else {
                this.currentUser = null;
                return null;
            }
        } catch (error) {
            console.error('Failed to load current user:', error);
            this.currentUser = null;
            return null;
        }
    }

    updateUserInterface() {
        const userElements = document.querySelectorAll('[data-user-field]');
        
        userElements.forEach(element => {
            const field = element.getAttribute('data-user-field');
            if (this.currentUser && this.currentUser[field]) {
                element.textContent = this.currentUser[field];
            }
        });

        // Show/hide authenticated elements
        const authElements = document.querySelectorAll('[data-auth-required]');
        authElements.forEach(element => {
            element.style.display = this.currentUser ? 'block' : 'none';
        });

        const noAuthElements = document.querySelectorAll('[data-no-auth-required]');
        noAuthElements.forEach(element => {
            element.style.display = this.currentUser ? 'none' : 'block';
        });
    }

    async requireAuthentication() {
        const isAuthenticated = await this.validateSession();
        
        if (!isAuthenticated) {
            const currentPath = window.location.pathname + window.location.search;
            window.location.href = `/login/?next=${encodeURIComponent(currentPath)}`;
            return false;
        }
        
        await this.loadCurrentUser();
        return true;
    }

    async logout() {
        try {
            await this.authService.logout();
        } catch (error) {
            console.error('Logout request failed:', error);
        } finally {
            // Always redirect to login, even if logout request failed
            window.location.href = '/login/';
        }
    }
}

// Global instance
window.sessionManager = new SessionManager();

// Auto-validate session on protected pages
document.addEventListener('DOMContentLoaded', function() {
    const protectedPage = document.body.hasAttribute('data-auth-required');
    
    if (protectedPage) {
        window.sessionManager.requireAuthentication();
    } else {
        // Optional: Load user data if available
        window.sessionManager.loadCurrentUser();
    }
});
```

## Template Integration

### Base Template

```html
<!-- templates/base_auth.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Cielo{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body {% block body_attrs %}{% endblock %}>
    <nav class="navbar">
        <div class="nav-brand">
            <a href="/">Cielo</a>
        </div>
        <div class="nav-links">
            <!-- Authentication-aware navigation -->
            <div data-no-auth-required>
                <a href="/login/">Login</a>
            </div>
            <div data-auth-required style="display: none;">
                <span>Welcome, <span data-user-field="username"></span></span>
                <a href="#" onclick="window.sessionManager.logout()">Logout</a>
            </div>
        </div>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Load authentication scripts -->
    <script src="{% static 'js/auth-service.js' %}"></script>
    <script src="{% static 'js/session.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Login Template

```html
<!-- templates/users/login.html -->
{% extends 'base_auth.html' %}
{% load static %}

{% block title %}Login - Cielo{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-form">
        <h2>Login to Cielo</h2>
        
        <div id="login-error" class="error-message" style="display: none;"></div>
        
        <form id="login-form">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" id="login-submit" class="btn btn-primary">
                Login
            </button>
        </form>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/login.js' %}"></script>
{% endblock %}
```

### Protected Page Template

```html
<!-- templates/dashboard.html -->
{% extends 'base_auth.html' %}
{% load static %}

{% block title %}Dashboard - Cielo{% endblock %}

{% block body_attrs %}data-auth-required{% endblock %}

{% block content %}
<div class="dashboard">
    <h1>Dashboard</h1>
    
    <div class="user-info">
        <h3>Welcome back, <span data-user-field="first_name">User</span>!</h3>
        <p>Email: <span data-user-field="email"></span></p>
    </div>
    
    <div class="dashboard-widgets">
        <!-- Dashboard content -->
        <div class="widget">
            <h4>Recent Activity</h4>
            <div id="recent-activity">
                <!-- Content loaded via AJAX -->
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/dashboard.js' %}"></script>
{% endblock %}
```

## Error Handling

### JavaScript Error Handling

```javascript
// static/js/error-handler.js
class ErrorHandler {
    static handle(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        if (error.status === 401) {
            // Unauthorized - redirect to login
            this.redirectToLogin();
        } else if (error.status === 403) {
            // Forbidden - show access denied
            this.showError('Access denied. You do not have permission to perform this action.');
        } else if (error.status >= 500) {
            // Server error
            this.showError('Server error. Please try again later.');
        } else if (error.status === 0) {
            // Network error
            this.showError('Network error. Please check your connection.');
        } else {
            // Other errors
            this.showError(error.error || 'An unexpected error occurred.');
        }
    }

    static redirectToLogin() {
        const currentPath = window.location.pathname + window.location.search;
        window.location.href = `/login/?next=${encodeURIComponent(currentPath)}`;
    }

    static showError(message, duration = 5000) {
        // Create or update error notification
        let errorDiv = document.getElementById('global-error');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'global-error';
            errorDiv.className = 'error-notification';
            document.body.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide after duration
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, duration);
    }
}

// Global error handler
window.addEventListener('unhandledrejection', function(event) {
    ErrorHandler.handle(event.reason, 'unhandled promise rejection');
});
```

## Security Considerations

### CSRF Protection

While the frontend doesn't handle authentication directly, ensure CSRF tokens are available for any form submissions:

```javascript
// Get CSRF token for requests
function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : null;
}
```

### Content Security Policy

Configure CSP headers to allow communication with identity provider:

```python
# In settings
CSP_DEFAULT_SRC = ["'self'"]
CSP_SCRIPT_SRC = ["'self'", "'unsafe-inline'"]
CSP_CONNECT_SRC = ["'self'", "http://identity.cielo.test"]
CSP_IMG_SRC = ["'self'", "data:"]
```

### Input Validation

Always validate and sanitize user inputs on the frontend:

```javascript
function sanitizeInput(input) {
    return input.trim().replace(/[<>]/g, '');
}
```

## Testing Authentication

### Frontend Unit Tests

```javascript
// tests/js/auth-service.test.js
describe('AuthService', () => {
    let authService;
    
    beforeEach(() => {
        authService = new AuthService();
        global.fetch = jest.fn();
    });
    
    test('login makes correct API call', async () => {
        fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve({ user: { username: 'testuser' } })
        });
        
        const result = await authService.login('testuser', 'password');
        
        expect(fetch).toHaveBeenCalledWith(
            'http://identity.cielo.test/login/',
            expect.objectContaining({
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify({ username: 'testuser', password: 'password' })
            })
        );
        
        expect(result.ok).toBe(true);
    });
});
```

### Integration Tests

```python
# tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse

class FrontendViewTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login to Cielo')
    
    def test_dashboard_page_renders(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        # Note: Authentication is handled by JavaScript
```

## Troubleshooting

### Common Issues

1. **Session not persisting across requests**
   - Check `SESSION_COOKIE_DOMAIN = ".cielo.test"`
   - Verify browser allows third-party cookies
   - Ensure identity provider is setting cookies correctly

2. **CORS errors in browser console**
   - Add identity provider domain to `CORS_ALLOWED_ORIGINS`
   - Verify `credentials: 'include'` in fetch requests
   - Check browser network tab for preflight requests

3. **JavaScript not loading user data**
   - Check browser console for errors
   - Verify session validation is working
   - Test API endpoints directly with curl

4. **Redirect loops on protected pages**
   - Ensure session validation logic is correct
   - Check for JavaScript errors preventing authentication
   - Verify identity provider endpoints are accessible

### Debug Tools

Add debug information to help troubleshoot:

```javascript
// Debug mode helper
if (window.location.search.includes('debug=true')) {
    window.debugAuth = true;
    console.log('Authentication debug mode enabled');
    
    // Log all authentication requests
    const originalMakeRequest = window.authService.makeRequest;
    window.authService.makeRequest = async function(...args) {
        console.log('Auth request:', args);
        const result = await originalMakeRequest.apply(this, args);
        console.log('Auth response:', result);
        return result;
    };
}
```

This documentation provides a complete guide for implementing and maintaining authentication features in the CieloFrontend Django project, ensuring seamless integration with the CieloIdentityProvider service.
