#!/usr/bin/env bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token/ -H 'Content-Type: application/json' -d '{"username":"admin","password":"Admin@123"}' | python -c "import sys,json; print(json.load(sys.stdin)['access'])")
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/dashboards/cxo/
