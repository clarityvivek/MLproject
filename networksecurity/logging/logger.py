#logs are the tracks of every activity happening in the huge blocks of codes so if there's an error any random time, we can look at the last log warning or info etc to fix

import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"        #name of the log file to be created e.g. 12_6_2025_12_30_10.log

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
#cwd = current working directory , logs is the folder name
os.makedirs(logs_path,exist_ok=True)
#exist_ok=True means if there's a directory named "log_path" that already exists , don't create again
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)