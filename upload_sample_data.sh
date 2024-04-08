#!/usr/bin/env bash
TOKEN=$(curl -d 'client_id=m4i_public' -d "username=$KEYCLOAK_USERNAME" -d "password=$KEYCLOAK_PASSWORD" -d 'grant_type=password' \
    "${KEYCLOAK_URL}realms/m4i/protocol/openid-connect/token" | jq .access_token)

curl -g -v -X POST -H "Authorization: Bearer ${TOKEN:1:-1}" \
                -H "Content-Type: multipart/form-data" \
                -H "Cache-Control: no-cache" \
                -F data=@data/sample_data.zip \
                "${ATLAS_URL}/admin/import"
