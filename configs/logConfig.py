import os
from datetime import datetime
from logging.config import dictConfig

# 確保 logs 資料夾存在
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = os.path.join(LOG_DIR, f'{current_time}.log')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_filename,
            # 'filename': os.path.join(LOG_DIR, 'app.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'formatter': 'default',
            'encoding': 'utf8'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']  # 同時輸出到螢幕和檔案
    }
})