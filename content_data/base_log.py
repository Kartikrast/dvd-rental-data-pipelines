import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

log_dir = os.path.dirname(os.path.abspath(__file__)) 

class Logger:
    def __init__(self, pipeline_name: str, log_dir: str = log_dir+"/tmdb_logs"):
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        log_file = Path(log_dir) / f"{pipeline_name}.csv"

        self.logger = logging.getLogger(pipeline_name)
        self.logger.setLevel(logging.DEBUG)
        

        if not self.logger.handlers:
            if not os.path.exists(log_file):
                with open(log_file, "w", encoding="utf-8") as f:
                    f.write("timestamp,module,level,message\n")
            
            file_handler = RotatingFileHandler(
                log_file, maxBytes=1_000_000, backupCount=5, encoding="utf-8"
            )

            console_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s,%(name)s,%(levelname)s,%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
