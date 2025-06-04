// Auth utility functions for JWT token handling

/**
 * Get the current access token from localStorage
 * @returns {string|null} The access token or null if not found
 */
function getAccessToken() {
  return localStorage.getItem('access_token');
}

/**
 * Get the current refresh token from localStorage
 * @returns {string|null} The refresh token or null if not found
 */
function getRefreshToken() {
  return localStorage.getItem('refresh_token');
}

/**
 * Get the current user data from localStorage
 * @returns {object|null} The user data or null if not found
 */
function getCurrentUser() {
  const userData = localStorage.getItem('user');
  return userData ? JSON.parse(userData) : null;
}

/**
 * Add authorization header to fetch options
 * @param {object} options - Fetch options object
 * @returns {object} Updated options with authorization header
 */
function withAuth(options = {}) {
  const accessToken = getAccessToken();
  if (!accessToken) return options;
  
  return {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`
    }
  };
}

/**
 * Make an authenticated API request
 * @param {string} url - The URL to fetch
 * @param {object} options - Fetch options
 * @returns {Promise} The fetch promise
 */
async function authFetch(url, options = {}) {
  const authOptions = withAuth(options);
  const response = await fetch(url, authOptions);
  
  if (response.status === 401) {
    // Token expired, try to refresh
    const refreshed = await refreshTokens();
    if (refreshed) {
      // Retry with new token
      return fetch(url, withAuth(options));
    } else {
      // Redirect to login
      window.location.href = '/users/login/';
    }
  }
  
  return response;
}

/**
 * Try to refresh the access token using the refresh token
 * @returns {Promise<boolean>} Whether the refresh was successful
 */
async function refreshTokens() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;
  
  try {
    const resp = await fetch(`${window.IDENTITY_BASE}/api/token/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken })
    });
    
    if (resp.ok) {
      const tokens = await resp.json();
      localStorage.setItem('access_token', tokens.access);
      if (tokens.refresh) {
        localStorage.setItem('refresh_token', tokens.refresh);
      }
      return true;
    } else {
      // Token refresh failed (expired, blacklisted, etc.)
      // Clear tokens and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      return false;
    }
  } catch (err) {
    console.error('Token refresh error:', err);
    // Clear tokens on error
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    return false;
  }
}

// Export the auth utilities
window.CieloAuth = {
  getAccessToken,
  getRefreshToken,
  getCurrentUser,
  withAuth,
  authFetch,
  refreshTokens
};
