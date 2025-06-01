function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

fetch('/api/logout', {
  method: 'POST',
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  },
  credentials: 'same-origin'
}).then(() => {
  // optional success handling
});
