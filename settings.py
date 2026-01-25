
import json
from pathlib import Path

class Settings:
  def __init__(self, path="settings.json", defaults=None):
    self.path = Path(path)
    self.data = defaults.copy() if defaults else {}
    self.load()

  def load(self):
    if self.path.exists():
      with self.path.open("r", encoding="utf-8") as f:
        self.data.update(json.load(f))
    else:
      self.save()

  def save(self):
    self.path.parent.mkdir(parents=True, exist_ok=True)
    with self.path.open("w", encoding="utf-8") as f:
      json.dump(self.data, f, indent=4)
    print("settings saved")

  def get(self, key, default=None):
    return self.data.get(key, default)

  def set(self, key, value):
    self.data[key] = value
    self.save()
    print(key, "set to", value)


# usage
defaults = {
  "default_language_code": "en",
  "token_order": 0,
}

settings = Settings("config/settings.json", defaults)



