from datetime import datetime, timedelta, timezone

from config import Config
from opensearch import OpenSearchClient
from mail import MailClient


def main():

    print("=" * 60)
    print("Iniciando Wazuh Notifier")
    print("=" * 60)

    config = Config()

    notification_rules = set(
        config.notifications.get("rules", [])
    )

    print(f"OpenSearch Host : {config.opensearch['host']}")
    print(f"OpenSearch Port : {config.opensearch['port']}")

    client = OpenSearchClient(config)
    mail = MailClient(config)

    timestamp = (
        datetime.now(timezone.utc)
        - timedelta(minutes=config.polling["interval"])
    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    alerts = client.get_alerts_since(timestamp)

    print()
    print(f"{len(alerts)} alertas encontrados")
    print()

    for alert in alerts:

        source = alert["_source"]

        rule = source.get("rule", {})
        agent = source.get("agent", {})
        syscheck = source.get("syscheck", {})

        rule_id = int(rule.get("id", 0))

        if notification_rules and rule_id not in notification_rules:
            continue

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