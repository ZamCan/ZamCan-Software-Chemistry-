import pytest

from knowledge.elements.loaders import (
    ElementDataSource,
    ElementSourceCatalog,
    RawElementRecord,
)


class TestSource(ElementDataSource):
    name = "test-source"
    authority = "test"

    def records(self):
        return (
            RawElementRecord(
                atomic_number=1,
                name="Hydrogen",
                symbol="H",
            ),
        )


def test_source_contract():
    source = TestSource()

    assert source.name == "test-source"
    assert source.authority == "test"
    assert len(source.records()) == 1


def test_source_validation():
    TestSource().validate()


def test_source_catalog():
    catalog = ElementSourceCatalog()
    source = TestSource()

    catalog.register(source)

    assert catalog.get("test-source") is source
    assert catalog.all() == (source,)


def test_duplicate_source_rejected():
    catalog = ElementSourceCatalog()
    source = TestSource()

    catalog.register(source)

    with pytest.raises(ValueError):
        catalog.register(source)
