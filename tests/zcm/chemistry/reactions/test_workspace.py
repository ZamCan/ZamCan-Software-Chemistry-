from zcm.chemistry.reactions import reaction_workspace


def test_workspace_balances_equation():
    result = reaction_workspace.balance(
        ("H2", "O2"),
        ("H2O",),
    )

    assert result.formatted() == "2H2 + O2 → 2H2O"


def test_workspace_assesses_reaction():
    result = reaction_workspace.assess(
        ("He", "F2"),
    )

    assert result.primary_reason is not None
