class NotificationPolicy:

    def __init__(self, rules: list[int], critical_paths: list[str]):

        self.rules = set(rules)

        self.critical_paths = [
            path.lower()
            for path in critical_paths
        ]

    def should_notify(self, alert: dict) -> bool:

        """
        Retorna True se o alerta deve gerar uma notificação.
        """

        source = alert.get("_source", {})

        rule_id = int(
            source.get("rule", {}).get("id", 0)
        )

        if self.rules and rule_id not in self.rules:
            return False

        syscheck = source.get("syscheck", {})

        path = syscheck.get("path", "").lower()

        if self.critical_paths:
            return any(
                path.startswith(critical_path)
                for critical_path in self.critical_paths
            )

        return True