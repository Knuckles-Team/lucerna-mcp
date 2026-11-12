"""The k-NN tools are served only where the cluster's k-NN plugin is usable.

The homelab search nodes have no AVX2, so the plugin is disabled there and a k-NN
query fails. The tools are gated by ``LUCERNA_KNN_ENABLED`` (default off) instead of
being served and failing; ``lucerna_knn_plugin_enabled`` reports the cluster state.
"""

from __future__ import annotations

from scion_sdk.config import setting
from scion_sdk.utilities import to_boolean

KNN_SETTING = "LUCERNA_KNN_ENABLED"
KNN_METHODS = frozenset({"knn_search"})


def knn_enabled() -> bool:
    """True when the operator declared that the cluster's k-NN plugin works."""
    return to_boolean(setting(KNN_SETTING, "false"))
