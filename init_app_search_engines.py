import os

import requests
from elastic_enterprise_search import AppSearch
from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth

from app_search_engine_setup import engines


NAMESPACE = os.getenv("NAMESPACE", "demo")

elastic_url = os.getenv(
    "ELASTIC_URL", f"http://elastic-search-es-http.{NAMESPACE}.svc.cluster.local:9200/"
)
enterprise_search_url = os.getenv(
    "ENTERPRISE_SEARCH_EXTERNAL_URL",
    f"http://enterprise-search-ent-http.${NAMESPACE}.svc.cluster.local:3002/",
)
elastic_username = os.getenv("ELASTIC_USERNAME", "elastic")
elastic_password = os.getenv("ELASTIC_PASSWORD", "elastic")


def get_enterprise_api_private_key(
    enterprise_search_url, elastic_username, elastic_password
):
    key_response = requests.get(
        f"{enterprise_search_url}api/as/v1/credentials/private-key",
        auth=HTTPBasicAuth(elastic_username, elastic_password),
    )
    key_info = key_response.json()
    return key_info["key"]


def put_index_template(elastic_client):
    elastic_client.indices.put_index_template(
        name="atlas-dev-template",
        index_patterns=[".ent-search-engine-documents-atlas-dev"],
        priority=1,
        template={
            "mappings": {
                "dynamic_templates": [
                    {
                        "select_fields_as_keywords": {
                            "match_mapping_type": "*",
                            "match": "*guid*",
                            "mapping": {"type": "keyword"},
                        }
                    }
                ]
            }
        },
    )


def create_engines(app_search_client):
    for engine in engines:
        app_search_client.create_engine(engine["name"])
        app_search_client.put_schema(engine["name"], engine["schema"])
        app_search_client.put_search_settings(engine["name"], engine["search-settings"])


def main():
    elastic_client = Elasticsearch(
        hosts=[elastic_url], basic_auth=(elastic_username, elastic_password)
    )

    put_index_template(elastic_client)

    app_search_api_key = get_enterprise_api_private_key(
        enterprise_search_url, elastic_username, elastic_password
    )

    app_search_client = AppSearch(enterprise_search_url, bearer_auth=app_search_api_key)

    create_engines(app_search_client)


if __name__ == "__main__":
    main()
