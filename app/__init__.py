def __init__(self, config: Config):

    self.client = OpenSearch(

        hosts=[
            {
                "host": config.opensearch["host"],
                "port": config.opensearch["port"]
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