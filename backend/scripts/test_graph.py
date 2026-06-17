import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.workflows.support_workflow import graph


result = graph.invoke(
    {
        "question": "How long do refunds take?",
        "history": []
    }
)

print(result)