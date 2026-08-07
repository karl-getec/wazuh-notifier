from datetime import datetime, timedelta, timezone

from config import Config
from mail import MailClient
from opensearch import OpenSearchClient
from policy import NotificationPolicy


def main():

    print("=" * 60)
    print("Iniciando Wazuh Notifier")
    print("=" * 60)

    config = Config()

    print(f"OpenSearch Host : {config.opensearch['host']}")
    print(f"OpenSearch Port : {config.opensearch['port']}")

    client = OpenSearchClient(config)
    mail = MailClient(config)

    policy = NotificationPolicy(
        rules=config.notifications.get("rules", []),
        critical_paths=config.notifications.get("critical_paths", [])
    )

    timestamp = (
        datetime.now(timezone.utc)
        - timedelta(minutes=config.polling["interval"])
    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    alerts = client.get_alerts_since(timestamp)

    print()
    print(f"{len(alerts)} alertas encontrados")
    print()

    for alert in alerts:

        if not policy.should_notify(alert):
            continue

        source = alert["_source"]

        rule = source.get("rule", {})
        agent = source.get("agent", {})
        syscheck = source.get("syscheck", {})

        print("=" * 60)

        print(f"Timestamp : {source.get('timestamp')}")
        print(f"Rule      : {rule.get('id')}")
        print(f"Descrição : {rule.get('description')}")
        print(f"Agente    : {agent.get('name')}")

        if syscheck:
            print(f"Arquivo   : {syscheck.get('path')}")

        subject = f"Wazuh Alert - Rule {rule.get('id')}"

        body = f"""
Timestamp : {source.get('timestamp')}

Rule      : {rule.get('id')}
Descrição : {rule.get('description')}

Agente    : {agent.get('name')}

Arquivo   : {syscheck.get('path')}
"""

        mail.send(subject, body)

    print()
    print("Finalizado com sucesso.")


if __name__ == "__main__":
    main()