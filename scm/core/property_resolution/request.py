from __future__ import annotations

from dataclasses import dataclass

from scm.core.conditions import Conditions
from scm.core.property_kind import PropertyKind


@dataclass(frozen=True)
class PropertyRequest:
    """
    Scientific request for resolving one property.

    Identity and conditions are separated deliberately:
    multiple scientific records may represent the same property
    identity under different conditions or with different evidence.
    """

    kind: PropertyKind
    conditions: Conditions | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, PropertyKind):
            raise TypeError(
                "kind must be a PropertyKind"
            )

        if (
            self.conditions is not None
            and not isinstance(self.conditions, Conditions)
        ):
            raise TypeError(
                "conditions must be a Conditions instance or None"
            )


__all__ = [
    "PropertyRequest",
]
