#!/usr/bin/env bash
TOKEN=$(curl -d "client_id=$KEYCLOAK_CLIENT_ID" -d "username=$KEYCLOAK_USERNAME" -d "password=$KEYCLOAK_ATLAS_ADMIN_PASSWORD" -d 'grant_type=password' \
    "${KEYCLOAK_SERVER_URL}realms/${KEYCLOAK_REALM_NAME}/protocol/openid-connect/token" | jq .access_token)

curl -g -v -X POST -H "Authorization: Bearer ${TOKEN:1:-1}" \
                -H "Content-Type: multipart/form-data" \
                -H "Cache-Control: no-cache" \
                -F data=@data/sample_data.zip \
                "${ATLAS_SERVER_URL}/admin/import"
