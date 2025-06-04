function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

const form = document.getElementById('login-form');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);
  const resp = await fetch(`${window.IDENTITY_BASE}/api/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data),
    credentials: 'include'
  });
  
  if (resp.ok) {
    const tokens = await resp.json();
    
    // Store tokens in localStorage
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    
    // Store user data if available
    if (tokens.user) {
      localStorage.setItem('user', JSON.stringify(tokens.user));
    }
    
    window.location.href = '/';
  } else {
    document.getElementById('login-error').innerText = 'Invalid credentials.';
  }
});
