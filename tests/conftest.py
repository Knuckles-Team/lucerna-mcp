"""Test configuration: the full served surface.

The k-NN search tool is served only where the operator declares the cluster's k-NN
plugin usable (``LUCERNA_KNN_ENABLED``). The tool-use contracts, links and prompts
name that tool, so the connector conformance run builds the server with it served.
"""

import os

os.environ.setdefault("LUCERNA_KNN_ENABLED", "true")
