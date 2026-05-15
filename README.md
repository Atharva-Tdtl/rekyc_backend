# Agentic AI KYC / Re-KYC Backend PoC (Django REST)

This backend implements functional modules for the Housing Finance KYC/Re-KYC automation UI.

## Modules
- Customer onboarding and profile management
- Document intake, classification, OCR-style extraction mock
- Identity verification, address verification, video KYC and field verification
- AML/risk scoring, fraud detection and sanctions/PEP/adverse media mock checks
- Maker-checker workflow and case management
- CKYC registry mock integration
- Compliance dashboard, operations dashboard and CXO dashboard APIs
- Audit logs, alerts and communication templates
- RBAC-oriented roles: Admin, CXO, Operations, Compliance, Branch User, Field Agent

## Quick setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

API root: `http://localhost:8000/api/`

Swagger/OpenAPI schema: `http://localhost:8000/api/schema/`

## Demo users
Created by `seed_demo`:

| Role | Username | Password |
|---|---|---|
| Admin | admin | Admin@123 |
| Operations | ops_user | Ops@123 |
| Compliance | compliance_user | Compliance@123 |
| CXO | cxo_user | Cxo@123 |
| Field Agent | field_agent | Field@123 |

## Important endpoints

- `POST /api/auth/token/`
- `GET/POST /api/customers/`
- `POST /api/customers/{id}/submit/`
- `GET/POST /api/documents/`
- `POST /api/documents/{id}/process/`
- `POST /api/verification/identity/run/`
- `POST /api/verification/address/run/`
- `POST /api/risk/score/{customer_id}/`
- `POST /api/risk/fraud/{customer_id}/`
- `POST /api/workflow/cases/{id}/approve/`
- `POST /api/workflow/cases/{id}/reject/`
- `GET /api/dashboards/cxo/`
- `GET /api/dashboards/operations/`
- `GET /api/dashboards/compliance/`

## Environment notes
This PoC uses SQLite and mock integrations for Aadhaar offline XML, PAN, CKYC, DigiLocker, sanctions/PEP and adverse media. Replace service classes in `apps/integrations/services.py` and `apps/risk/services.py` with production connectors.
