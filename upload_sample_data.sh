#!/usr/bin/env bash
TOKEN=$(curl -d "client_id=$KEYCLOAK_CLIENT_ID" -d "username=$KEYCLOAK_USERNAME" -d "password=$KEYCLOAK_ATLAS_ADMIN_PASSWORD" -d 'grant_type=password' \
    "${KEYCLOAK_SERVER_URL}realms/${KEYCLOAK_REALM_NAME}/protocol/openid-connect/token" | jq .access_token)

python export_atlas.py --token "$TOKEN" \
--base-url "$ATLAS_SERVER_URL"\
--output "data/sample_data.zip"
