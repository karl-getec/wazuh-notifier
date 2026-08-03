from config import Config
from opensearch import OpenSearchClient
from policy import NotificationPolicy


def main():

    config = Config()

    client = OpenSearchClient(config)

    policy = NotificationPolicy(
        rules=config.notifications["rules"],
        critical_paths=config.notifications["critical_paths"]
    )

    alerts = client.get_latest_alerts()

    print("=" * 70)
    print(f"{len(alerts)} alertas encontrados")
    print("=" * 70)

    for alert in alerts:

        source = alert.get("_source", {})

        rule = source.get("rule", {})
        syscheck = source.get("syscheck", {})
        agent = source.get("agent", {})

        print()

        print(f"Data.......: {source.get('timestamp')}")
        print(f"Rule.......: {rule.get('id')}")
        print(f"Descrição..: {rule.get('description')}")
        print(f"Agente.....: {agent.get('name', '-')}")
        print(f"Arquivo....: {syscheck.get('path', '-')}")

        if policy.should_notify(alert):
            print(">>> ALERTA CRÍTICO - Enviar e-mail <<<")

        print("-" * 70)


if __name__ == "__main__":
    main()