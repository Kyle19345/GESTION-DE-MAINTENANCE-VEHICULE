# logger_config.py
import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def setup_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO

    # Formatter commun
    fmt = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    # Root logger
    root = logging.getLogger()
    root.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # Rotating file handler (10MB, 5 backups)
    fh = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setLevel(logging.DEBUG)  # on garde DEBUG dans le fichier pour traçage complet
    fh.setFormatter(formatter)
    root.addHandler(fh)

    # Optionnel : réduire le bruit des bibliothèques
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("tkinter").setLevel(logging.WARNING)

    return root
