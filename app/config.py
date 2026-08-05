from pathlib import Path
import os
import yaml


class Config:

    def __init__(self):

        config_file = os.getenv("CONFIG_FILE")

        if config_file:
            self.path = Path(config_file)
        else:
            self.path = Path(__file__).parent.parent / "config" / "app.yaml"

        if not self.path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self.path}"
            )

        with open(self.path, "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)

        self._load_environment()

    def _load_environment(self):

        opensearch = self.data.setdefault("opensearch", {})

        opensearch["host"] = os.getenv(
            "OPENSEARCH_HOST",
            opensearch.get("host")
        )

        opensearch["port"] = int(
            os.getenv(
                "OPENSEARCH_PORT",
                opensearch.get("port", 9200)
            )
        )

        opensearch["username"] = os.getenv(
            "OPENSEARCH_USERNAME",
            opensearch.get("username")
        )

        opensearch["password"] = os.getenv(
            "OPENSEARCH_PASSWORD",
            opensearch.get("password")
        )

        verify = os.getenv("OPENSEARCH_VERIFY_CERTS")

        if verify is not None:
            opensearch["verify_certs"] = verify.lower() == "true"

        smtp = self.data.setdefault("smtp", {})

        smtp["host"] = os.getenv(
            "SMTP_HOST",
            smtp.get("host")
        )

        smtp["port"] = int(
            os.getenv(
                "SMTP_PORT",
                smtp.get("port", 587)
            )
        )

        smtp["username"] = os.getenv(
            "SMTP_USERNAME",
            smtp.get("username")
        )

        smtp["password"] = os.getenv(
            "SMTP_PASSWORD",
            smtp.get("password")
        )

        smtp["enabled"] = os.getenv(
            "SMTP_ENABLED",
            str(smtp.get("enabled", False))
        ).lower() == "true"

        smtp["sender"] = os.getenv(
            "SMTP_SENDER",
            smtp.get("sender")
        )

        smtp["recipients"] = smtp.get("recipients", [])

    @property
    def opensearch(self):
        return self.data.get("opensearch", {})

    @property
    def polling(self):
        return self.data.get("polling", {})

    @property
    def notifications(self):
        return self.data.get("notifications", {})

    @property
    def smtp(self):
        return self.data.get("smtp", {})