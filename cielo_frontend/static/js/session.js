(async function() {
  // Load the auth utilities
  const CieloAuth = window.CieloAuth;
  
  if (!CieloAuth) {
    console.error('CieloAuth not loaded! Make sure auth.js is included before session.js');
    window.location.href = '/users/login/';
    return;
  }
  
  try {
    // Check if we have an access token
    const accessToken = CieloAuth.getAccessToken();
    
    if (!accessToken) {
      window.location.href = '/users/login/';
      return;
    }
    
    // Verify the token by making a request to fetch current user
    try {
      // Use the authFetch utility which handles token refresh automatically
      const resp = await CieloAuth.authFetch(`${window.IDENTITY_BASE}/api/users/me`);
      
      if (!resp.ok) {
        console.error('Session verification failed');
        window.location.href = '/users/login/';
        return;
      }
      
      // Store the latest user data
      const userData = await resp.json();
      localStorage.setItem('user', JSON.stringify(userData));
      
    } catch (fetchErr) {
      console.error('Session fetch error:', fetchErr);
      window.location.href = '/users/login/';
    }
  } catch (err) {
    console.error('Session check error:', err);
    window.location.href = '/users/login/';
  }
})();
