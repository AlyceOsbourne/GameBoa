import pprint
import traceback

from project.src.system.event_handler import EventHandler
from project.src.system.events import SystemEvents
from tkinter import messagebox

# url with attachment
url = "https://github.com/AlyceOsbourne/GameBoa/issues/new?title={title}&body={body}"


@EventHandler.subscriber(SystemEvents.ExceptionRaised)
def handle_exception(exception):
    send_to_dev = messagebox.askyesno(
        "Exception",
        "An exception has been raised. Would you like to send it to the developers?",
        detail=exception,
        default=messagebox.NO
    )
    if send_to_dev:
        import webbrowser
        import json

        title = "Exception: " + str(exception)
        formatteded_exception = "```python\n" + pprint.pformat(exception) + "\n```\n\n"
        tb = traceback.format_tb(exception.__traceback__)
        formatted_tb = "```python\n" + "".join(tb) + "\n```\n\n"
        body = formatteded_exception + formatted_tb
        body = json.dumps(body)[1:-1].replace("\\n", "%0A").replace("\\t", "%09")
        webbrowser.open(url.format(title=title, body=body))





