# Groc-Pal
This is Repository for Flask based Grocery Application.


Technical Aspects and Terms: 

🔧 Tech Stack

Backend Framework: Flask (Application Factory Pattern)

Database: SQLite with Flask-SQLAlchemy ORM

API Framework: Flask-Smorest (Blueprint-based REST APIs)

Authentication: JWT-based Stateless Authentication (Flask-JWT-Extended)

Validation Layer: Marshmallow (Request / Response Schema Enforcement)

Security: Password Hashing using Werkzeug

Deployment: Docker Containerized Application deployed on Microsoft Azure

Environment Management: python-dotenv (.env based secret management)

API Documentation: OpenAPI 3.0 (Swagger UI via Flask-Smorest)

🏗️ Architectural Design

Modular Blueprint-based REST API architecture

Service Layer abstraction for business logic isolation

Role-Based Access Control (RBAC) using JWT claims

Separation of Web Routes and API Transport Layer

Stateless Session Management using Access & Refresh Tokens

Environment-driven configuration for secrets

🔐 Security Implementations

JWT Access Token + Refresh Token Authentication

Token Expiry with configurable decode leeway

Logout with Token Revocation (JWT Blocklist using JTI)

Refresh Token Revocation Support

Write-Only Password Storage Pattern

Role-based Authorization (Admin-restricted API mutations)

Secure Secret Management via Environment Variables

TLS-encrypted external transport (Azure Edge Termination)

🚀 API Capabilities

Versioned REST APIs (/api/v1)

CRUD Operations with Schema-validated Payloads

Pagination Support

Filtering & Sorting at DB-Query Level

Refresh Token Workflow for Silent Re-Authentication

OpenAPI-compliant Interactive API Documentation