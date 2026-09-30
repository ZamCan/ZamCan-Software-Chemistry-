from uuid import UUID, uuid4


def new_id() -> UUID:
    """Create a unique SCM scientific entity identifier."""
    return uuid4()
