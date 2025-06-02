# 🧩 CIELO Frontend Developer Guide – Hybrid Django Template and JavaScript Architecture

This document explains how the `cielo_frontend` Django application is designed and how developers should work within it. The frontend is structured around **Django templates** that render the layout and structure of pages, while **JavaScript is used to dynamically populate content by consuming REST APIs** exposed by backend CIELO services.

The included JavaScript files and templates are illustrative examples. They demonstrate how to interact with the IdentityProvider APIs (`http://identity.cielo.test/api/login`, `http://identity.cielo.test/api/logout`, and `http://identity.cielo.test/api/session`) but can be adapted to suit your needs.

---

## 🎯 Purpose of `cielo_frontend`

The `cielo_frontend` app:

* Delivers server-rendered HTML templates as page shells (e.g., navigation, layout, sections)
* Acts as the login interface and user dashboard container
* Delegates content population to JavaScript, which calls REST APIs such as `cielo_identity_provider`, `cielo_inventory`, and `cielo_azure_billing`
* Maintains a session-authenticated user experience without using access tokens in JavaScript

> 🧠 **Note:** All authentication and identity flows are handled by the `cielo_identity_provider` service (formerly `cielo_users`). This service is responsible for session management, login/logout, and may eventually support third-party identity providers such as Azure Entra ID, GitHub, or GitLab. Frontend templates should treat it as the single source of truth for user authentication state.

---

## 🗂️ Directory Structure Overview

```bash
cielo_frontend/
├── cielo_frontend/             # Django project package
│   ├── settings/               # Modular settings (base/dev/prod)
│   ├── urls.py                 # URL routes
│   └── wsgi.py                 # WSGI entrypoint
├── templates/                  # Server-rendered HTML layout
│   ├── base.html               # Global layout
│   └── users/login.html        # Login page
├── static/                     # JavaScript/CSS assets
│   ├── css/styles.css
│   └── js/dashboard.js         # Example dynamic loader
├── requirements.txt            # Python dependencies
├── .envrc                      # direnv-managed virtualenv activation
├── .gitignore
└── manage.py
```

---

## 🔧 How to Develop Frontend Pages

### 1. Define a Template Shell

Templates only define structural layout:

```html
<!-- templates/servers/list.html -->
{% extends "base.html" %}
{% block content %}
  <h1>Servers</h1>
  <ul id="server-list">
    <li>Loading...</li>
  </ul>
  <script src="/static/js/servers.js"></script>
{% endblock %}
```

### 2. Add a JavaScript Content Loader

```js
// static/js/servers.js
fetch("/api/inventory/servers")
  .then(resp => resp.json())
  .then(data => {
    const list = document.getElementById("server-list");
    list.innerHTML = data.map(s => `<li>${s.name} (${s.status})</li>`).join("");
  });
```

### 3. Serve Template from a Simple View

In `urls.py`:

```python
from django.views.generic import TemplateView

urlpatterns = [
    path("servers/", TemplateView.as_view(template_name="servers/list.html")),
]
```

---

## 🌐 Communication with Backend APIs

All data displayed in templates comes from REST APIs:

* JavaScript fetches from services like `cielo_identity_provider`, `cielo_inventory`, etc.
* Authentication is handled via session (set on login)
* No tokens or API keys are exposed client-side
* You can use `fetch`, `axios`, or any JS method for API calls
* Protected pages should verify the active session by calling `http://identity.cielo.test/api/session` on load and redirect to `/users/login/` if the session is not valid.
* Core authentication endpoints:
  * `POST http://identity.cielo.test/api/login`
  * `POST http://identity.cielo.test/api/logout`
  * `GET  http://identity.cielo.test/api/session`

---

## ✅ Guidelines

* Use Django templates for layout and structure
* Use JavaScript for content rendering and dynamic updates
* Use `fetch()` to query authenticated REST APIs
* All apps share the same domain and session via cookies

---

## 🧪 Development Tips

* Use `runserver_plus` with `direnv` and `.venv`
* Templates live-reload on changes
* Static files in `static/` are served directly in dev via `STATICFILES_DIRS`
* Session cookie is automatically available in frontend JS requests

---

## 🚫 Anti-Patterns to Avoid

* ❌ Do not build full page content in Django views (only structure)
* ❌ Do not expose tokens or user credentials to JavaScript
* ❌ Do not build separate React/Vue SPAs unless explicitly needed
* ❌ Do not make unauthenticated API calls from the browser

---

This hybrid architecture ensures clean separation of concerns:

* Django handles routing, layout, and authentication
* JavaScript dynamically populates pages with user-specific data

It’s lightweight, secure, and scalable — the best of both worlds for CIELO’s frontend.

