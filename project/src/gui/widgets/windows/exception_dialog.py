import pprint
import traceback
from tkinter import messagebox

from project.src.system import SystemEvents

LINK_TO_ISSUES_ON_GITHUB = (
    "https://github.com/AlyceOsbourne/GameBoa/issues/new?title={title}&body={body}"
)


@SystemEvents.ExceptionRaised
def handle_exception(exception):
    report_issue_confirmed = messagebox.askyesno(
        "Report Issue Confirmation",
        "An issue has occured.\nWould you like to report it to the developers?",
        detail=exception,
        default=messagebox.YES,
    )

    if report_issue_confirmed:
        import json
        import webbrowser

        title = "Exception: " + str(exception)
        formatteded_exception = "```python\n" + pprint.pformat(exception) + "\n```\n\n"
        tb = traceback.format_tb(exception.__traceback__)
        formatted_tb = "```python\n" + "".join(tb) + "\n```\n\n"
        body = formatteded_exception + formatted_tb
        body = json.dumps(body)[1:-1].replace("\\n", "%0A").replace("\\t", "%09")
        webbrowser.open(LINK_TO_ISSUES_ON_GITHUB.format(title=title, body=body))
