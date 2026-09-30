from __future__ import annotations

from .base import ElementRecord
from .data.periodic_table import PeriodicElementData
from scm.matter.elements import Element


def build_element_record(
    data: PeriodicElementData,
) -> ElementRecord:
    """
    Build an ElementRecord from structured periodic-table data.

    Element identity is created from atomic number.
    Periodic classification comes from the dataset.
    """

    if not isinstance(data, PeriodicElementData):
        raise TypeError(
            "data must be a PeriodicElementData"
        )

    return ElementRecord(
        element=Element(data.atomic_number),
        name=data.name,
        symbol=data.symbol,
        period=data.period,
        group=data.group,
        block=data.block,
        category=data.category,
    )


__all__ = [
    "build_element_record",
]
