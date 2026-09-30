from zcm.interfaces.web.app import element_payload


def test_ui_receives_all_118_elements():
    elements = element_payload()

    assert len(elements) == 118


def test_ui_element_identity():
    elements = element_payload()

    hydrogen = elements[0]

    assert hydrogen["atomic_number"] == 1
    assert hydrogen["symbol"] == "H"
    assert hydrogen["name"] == "Hydrogen"


def test_ui_last_element():
    elements = element_payload()

    oganesson = elements[-1]

    assert oganesson["atomic_number"] == 118
    assert oganesson["symbol"] == "Og"


def test_ui_atomic_numbers_are_complete():
    elements = element_payload()

    numbers = {
        element["atomic_number"]
        for element in elements
    }

    assert numbers == set(range(1, 119))
