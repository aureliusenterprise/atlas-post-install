import asyncio
import os

from m4i_atlas_core import (
    ConfigStore,
    create_type_defs,
    data_dictionary_types_def,
    process_types_def,
    connectors_types_def,
    kubernetes_types_def,
    get_keycloak_token,
)

NAMESPACE = os.getenv("NAMESPACE", "demo")

store = ConfigStore.get_instance()

store.load(
    {
        "atlas.credentials.username": os.getenv("KEYCLOAK_ATLAS_USERNAME", "atlas"),
        "atlas.credentials.password": os.getenv("KEYCLOAK_ATLAS_PASSWORD", "atlas"),
        "atlas.server.url": os.getenv(
            "ATLAS_URL", f"http://atlas.{NAMESPACE}.svc.cluster.local:21000/api/atlas"
        ),
        "keycloak.server.url": os.getenv(
            "KEYCLOAK_URL", f"http://keycloak.{NAMESPACE}.svc.cluster.local:8080/auth/"
        ),
        "keycloak.client.id": "m4i_public",
        "keycloak.realm.name": "m4i",
        "keycloak.client.secret.key": None,
    }
)

atlas_user, atlas_password = store.get_many(
    "atlas.credentials.username", "atlas.credentials.password", all_required=True
)
access_token = get_keycloak_token(
    keycloak=None, credentials=(atlas_user, atlas_password)
)
# creation of type deinitions breaks at the moment because the m4i_atlas_core handle_requests is only
# capable of sending http requests to port 80
asyncio.run(create_type_defs(data_dictionary_types_def, access_token=access_token))
asyncio.run(create_type_defs(process_types_def, access_token=access_token))
asyncio.run(create_type_defs(connectors_types_def, access_token=access_token))
asyncio.run(create_type_defs(kubernetes_types_def, access_token=access_token))
