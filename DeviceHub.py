import json
import logging
from app.app import app
app.config.from_object('app.config')
from app.accounts.login import settings

from event_hooks import event_hooks
event_hooks(app)

if __name__ == '__main__':
    logging.basicConfig(filename="logs/log.log", level=logging.INFO)
    app.run()
    from app.Utils import create_superuser
    create_superuser()