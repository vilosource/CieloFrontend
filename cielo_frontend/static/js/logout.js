function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

fetch(`${window.IDENTITY_BASE}/logout`, {
  method: 'POST',
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  },
  credentials: 'same-origin'
}).finally(() => {
  document.cookie = 'sessionid=; Max-Age=0; path=/; domain=.cielo.test';
  window.location.href = '/users/login/';
});
