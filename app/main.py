from config import Config
from opensearch import OpenSearchClient


def main():

    print("=" * 60)
    print("Iniciando Wazuh Notifier")
    print("=" * 60)

    config = Config()

    print(f"OpenSearch Host : {config.opensearch['host']}")
    print(f"OpenSearch Port : {config.opensearch['port']}")

    client = OpenSearchClient(config)

    alerts = client.get_latest_alerts()

    print()
    print(f"{len(alerts)} alertas encontrados")
    print()

    for alert in alerts:

        source = alert["_source"]

        print("=" * 60)

        print(f"Timestamp : {source.get('timestamp')}")

        rule = source.get("rule", {})
        print(f"Rule      : {rule.get('id')}")
        print(f"Descrição : {rule.get('description')}")

        agent = source.get("agent", {})
        print(f"Agente    : {agent.get('name')}")

        syscheck = source.get("syscheck")

        if syscheck:
            print(f"Arquivo   : {syscheck.get('path')}")

    print()
    print("Finalizado com sucesso.")


if __name__ == "__main__":
    main()