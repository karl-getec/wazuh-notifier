from pathlib import Path
import os
import yaml


class Config:

    def __init__(self):

        config_file = os.getenv("CONFIG_FILE")

        if config_file:
            self.path = Path(config_file)
        else:
            self.path = Path(__file__).parent.parent / "config.yaml"

        if not self.path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self.path}"
            )

        with open(self.path, "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)

    @property
    def opensearch(self):
        return self.data.get("opensearch", {})

    @property
    def polling(self):
        return self.data.get("polling", {})

    @property
    def notifications(self):
        return self.data.get("notifications", {})