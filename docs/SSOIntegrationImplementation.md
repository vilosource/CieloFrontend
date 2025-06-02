2025-06-02

## SSO Integration Updates

The frontend now verifies the active session on protected pages using `static/js/session.js`. Logout calls the identity provider to terminate the server session and then redirects the user back to the login page. Documentation was updated to clarify API endpoints and usage patterns.
