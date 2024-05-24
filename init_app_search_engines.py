import os
import logging
import requests
from elastic_enterprise_search import AppSearch
from elastic_enterprise_search.exceptions import BadRequestError
from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth

from app_search_engine_setup import engines
from index_template import publish_state_template


NAMESPACE = os.getenv("NAMESPACE", "demo")

elastic_url = os.getenv(
    "ELASTIC_URL", f"http://elastic-search-es-http.{NAMESPACE}.svc.cluster.local:9200/"
)
enterprise_search_url = os.getenv(
    "ENTERPRISE_SEARCH_URL",
    f"http://enterprise-search-ent-http.{NAMESPACE}.svc.cluster.local:3002/",
)
elastic_username = os.getenv("ELASTIC_USERNAME", "elastic")
elastic_password = os.getenv("ELASTIC_PASSWORD", "elastic")
elastic_certificate_path = os.getenv("ELASTIC_CERTIFICATE_PATH", None)


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
        name="publish-state-template",
        index_patterns=["publish_state"],
        priority=1,
        template=publish_state_template,
    )


def create_engines(app_search_client):
    for engine in engines:
        try:
            app_search_client.create_engine(engine_name=engine["name"])
            app_search_client.put_schema(
                engine_name=engine["name"], schema=engine["schema"]
            )
            app_search_client.put_search_settings(
                engine_name=engine["name"],
                search_fields=engine["search-settings"]["search_fields"],
                result_fields=engine["search-settings"]["result_fields"],
            )
        except BadRequestError as e:
            if e.body["errors"] == ["Name is already taken"]:
                logging.warning(
                    f'Skipping creation of {engine["name"]}. Engine already exists.'
                )
            else:
                raise e
        finally:
            app_search_client.put_schema(
                engine_name=engine["name"], schema=engine["schema"]
            )
            app_search_client.put_search_settings(
                engine_name=engine["name"],
                search_fields=engine["search-settings"]["search_fields"],
                result_fields=engine["search-settings"]["result_fields"],
            )


def main():
    elastic_client = Elasticsearch(
        hosts=[elastic_url], basic_auth=(elastic_username, elastic_password), ca_certs=elastic_certificate_path
    )

    put_index_template(elastic_client)

    app_search_api_key = get_enterprise_api_private_key(
        enterprise_search_url, elastic_username, elastic_password
    )

    app_search_client = AppSearch(enterprise_search_url, bearer_auth=app_search_api_key)

    create_engines(app_search_client)


if __name__ == "__main__":
    main()
