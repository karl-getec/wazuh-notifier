from opensearchpy import OpenSearch
from config import Config


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