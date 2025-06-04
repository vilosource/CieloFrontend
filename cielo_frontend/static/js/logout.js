function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

// Get the refresh token to blacklist it
const refreshToken = localStorage.getItem('refresh_token');
const accessToken = localStorage.getItem('access_token');

if (refreshToken) {
  // Send the refresh token to the backend to blacklist it
  fetch(`${window.IDENTITY_BASE}/api/token/logout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({ refresh: refreshToken })
  }).catch(err => {
    console.error('Logout error:', err);
  });
}

// Clear tokens from localStorage
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
localStorage.removeItem('user');

// Redirect to login page
window.location.href = '/users/login/';
