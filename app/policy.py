class NotificationPolicy:

    def __init__(self, rules: list[int], critical_paths: list[str]):
        self.rules = rules
        self.critical_paths = [path.lower() for path in critical_paths]

    def should_notify(self, alert: dict) -> bool:
        """
        Retorna True se o alerta deve gerar uma notificação.
        """

        source = alert.get("_source", {})

        # Verifica a regra
        rule = source.get("rule", {}).get("id")

        if rule not in self.rules:
            return False

        # Verifica se existe informação do syscheck
        syscheck = source.get("syscheck")

        if not syscheck:
            return False

        # Caminho do arquivo
        path = syscheck.get("path", "").lower()

        # Verifica se o caminho pertence às pastas críticas
        for critical_path in self.critical_paths:
            if path.startswith(critical_path):
                return True

        return False