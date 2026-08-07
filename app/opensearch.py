from time import sleep

from opensearchpy import OpenSearch
from opensearchpy.exceptions import ConnectionError

from config import Config

MAX_RETRIES = 3
RETRY_DELAY = 3


class OpenSearchClient:

    def __init__(self, config: Config):

        self.client = OpenSearch(
            hosts=[
                {
                    "host": config.opensearch["host"],
                    "port": config.opensearch["port"],
                    "scheme": "https"
                }
            ],
            http_auth=(
                config.opensearch["username"],
                config.opensearch["password"]
            ),
            use_ssl=True,
            verify_certs=config.opensearch.get("verify_certs", False),
            ssl_show_warn=False
        )

    def get_latest_alerts(self, size: int = 10):

        query = {
            "size": size,
            "sort": [
                {
                    "timestamp": {
                        "order": "desc"
                    }
                }
            ],
            "query": {
                "match_all": {}
            }
        }

        response = self.client.search(
            index="wazuh-alerts-*",
            body=query
        )

        return response["hits"]["hits"]

    def get_alerts_since(self, timestamp: str):

        query = {
            "size": 1000,
            "sort": [
                {
                    "timestamp": {
                        "order": "asc"
                    }
                }
            ],
            "query": {
                "range": {
                    "timestamp": {
                        "gte": timestamp
                    }
                }
            }
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.client.search(
                    index="wazuh-alerts-*",
                    body=query
                )

                return response["hits"]["hits"]

            except ConnectionError as error:

                print(
                    f"Falha ao conectar ao OpenSearch "
                    f"(tentativa {attempt}/{MAX_RETRIES}). "
                    f"{error}"
                )

                if attempt == MAX_RETRIES:
                    raise

                print(f"Nova tentativa em {RETRY_DELAY} segundos...")

                sleep(RETRY_DELAY)