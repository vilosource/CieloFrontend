(async function() {
  try {
    const resp = await fetch(`${window.IDENTITY_BASE}/api/session`, {
      credentials: 'include'
    });
    if (!resp.ok) {
      window.location.href = '/users/login/';
      return;
    }
    const data = await resp.json();
    if (!data || data.authenticated !== true) {
      window.location.href = '/users/login/';
    }
  } catch (err) {
    window.location.href = '/users/login/';
  }
})();
