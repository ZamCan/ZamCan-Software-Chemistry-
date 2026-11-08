from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sqlite3

from scm.chemistry import assign_oxidation_states, gibbs_free_energy
from scm.core import Quantity
from scm.lab_records import Measurement
from scm.notebook import LabNotebook
from scm.research import Dataset
from scm.robotics import simulate_transfers
from zcm.calculations import (
    calculate, calculate_dilution, calculate_mass_molarity, calculate_molarity, stoichiometry, titrate,
)
from zcm.reasoning import infer_concentration


def _lab_commands(parser):
    commands = parser.add_subparsers(dest="action", required=True)
    create = commands.add_parser("create")
    create.add_argument("title")
    create.add_argument("objective")
    commands.add_parser("list")
    for action in ("export", "measure", "note", "dataset", "summarize"):
        commands.add_parser(action).add_argument("experiment_id")

    measure = commands.choices["measure"]
    measure.add_argument("quantity")
    measure.add_argument("value", type=float)
    measure.add_argument("unit")
    measure.add_argument("--instrument")
    measure.add_argument("--uncertainty", type=float)
    note = commands.choices["note"]
    note.add_argument("text")
    note.add_argument("--conclusion", action="store_true")
    dataset = commands.choices["dataset"]
    for field in ("dataset_id", "version", "title", "source"):
        dataset.add_argument(field)
    dataset.add_argument("--license", default="")
    dataset.add_argument("--checksum", default="")
    summary = commands.choices["summarize"]
    summary.add_argument("quantity")
    summary.add_argument("unit")
    summary.add_argument("--save", action="store_true")


def _lab(args):
    notebook = LabNotebook(args.db)
    if args.action == "create":
        return asdict(notebook.create(args.title, args.objective))
    if args.action == "list":
        return notebook.list()
    experiment = args.experiment_id
    if args.action == "export":
        return notebook.export(experiment)
    if args.action == "summarize":
        result = notebook.summarize(experiment, args.quantity, args.unit)
        if args.save:
            result = {**result, "record_sequence": notebook.record_calculation(experiment, result)}
        return result
    if args.action == "measure":
        measurement = Measurement(
            args.quantity, args.value, args.unit, args.instrument, args.uncertainty
        )
        sequence = notebook.record_measurement(experiment, measurement)
    elif args.action == "note":
        sequence = notebook.record_note(experiment, args.text, conclusion=args.conclusion)
    else:
        dataset = Dataset(
            args.dataset_id, args.version, args.title, args.source, args.license, args.checksum
        )
        sequence = notebook.record_dataset(experiment, dataset)
    return {"record_sequence": sequence}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="zcm")
    parser.add_argument("--db", type=Path, default=Path("zcm-notebook.sqlite3"))
    commands = parser.add_subparsers(dest="command", required=True)

    oxidation = commands.add_parser("oxidation")
    oxidation.add_argument("formula")
    oxidation.add_argument("--charge", type=int, default=0)
    gibbs = commands.add_parser("gibbs")
    for name in ("delta_h", "delta_s", "temperature"):
        gibbs.add_argument(name, type=float)

    calc = commands.add_parser("calculate", help="Run a molar-mass or equation-balancing query")
    calc.add_argument("query")
    titration = commands.add_parser("titrate", help="Calculate analyte amount and concentration")
    for name in ("titrant_mol_l", "titrant_ml", "analyte_ml"):
        titration.add_argument(name, type=float)
    ratio_source = titration.add_mutually_exclusive_group()
    ratio_source.add_argument("--ratio", type=float, help="Analyte moles per titrant mole, default 1")
    ratio_source.add_argument("--equation", help="Derive the ratio from the supplied reaction")
    titration.add_argument("--titrant", help="Titrant formula in the reaction")
    titration.add_argument("--analyte", help="Analyte formula in the reaction")
    stoich = commands.add_parser("stoichiometry", help="Calculate limiting reagents and theoretical yields")
    stoich.add_argument("equation")
    stoich.add_argument("amounts_mol", help="JSON object mapping each reactant formula to its initial mol amount")
    concentration = commands.add_parser("molarity", help="Calculate molarity from solute amount")
    concentration.add_argument("amount", type=float)
    concentration.add_argument("--amount-unit", default="mol", choices=("mol", "mmol"))
    from_mass = commands.add_parser("mass-molarity", help="Calculate molarity from formula and mass")
    from_mass.add_argument("formula")
    from_mass.add_argument("mass", type=float)
    from_mass.add_argument("--mass-unit", default="g", choices=("kg", "g", "mg"))
    dilution = commands.add_parser("dilute", help="Calculate molarity after solvent addition")
    dilution.add_argument("stock", type=float)
    dilution.add_argument("--stock-unit", default="mol/L", choices=("mol/L", "mmol/L"))
    dilution.add_argument("aliquot", type=float)
    dilution.add_argument("--aliquot-unit", default="mL", choices=("mL", "L"))
    for command in (concentration, from_mass, dilution):
        command.add_argument("final_volume", type=float)
        command.add_argument("--volume-unit", default="mL", choices=("mL", "L"))

    reasoning = commands.add_parser("infer-concentration", help="Select a calculation from analytical evidence")
    reasoning.add_argument("evidence", help="JSON object containing the known measurements and facts")
    robot = commands.add_parser("simulate-transfers", help="Simulate a JSON liquid-transfer plan")
    robot.add_argument("plan", type=Path)
    for command in (calc, titration, stoich, robot, concentration, from_mass, dilution, reasoning):
        command.add_argument("--experiment", help="Save the result to this experiment ID")
    _lab_commands(commands.add_parser("lab", help="Record and analyze experiments"))

    args = parser.parse_args(argv)
    try:
        if args.command == "oxidation":
            print(assign_oxidation_states(args.formula, args.charge))
            return
        if args.command == "gibbs":
            print(gibbs_free_energy(args.delta_h, args.delta_s, args.temperature))
            return
        if args.command == "lab":
            result = _lab(args)
        else:
            if args.command == "calculate":
                result = calculate(args.query)
            elif args.command == "titrate":
                result = titrate(
                    args.titrant_mol_l, args.titrant_ml, args.analyte_ml, args.ratio,
                    equation=args.equation, titrant=args.titrant, analyte=args.analyte,
                )
            elif args.command == "stoichiometry":
                result = stoichiometry(args.equation, json.loads(args.amounts_mol, parse_float=str))
            elif args.command == "molarity":
                result = calculate_molarity(
                    Quantity(args.amount, args.amount_unit), Quantity(args.final_volume, args.volume_unit)
                )
            elif args.command == "mass-molarity":
                result = calculate_mass_molarity(
                    args.formula, Quantity(args.mass, args.mass_unit),
                    Quantity(args.final_volume, args.volume_unit),
                )
            elif args.command == "dilute":
                result = calculate_dilution(
                    Quantity(args.stock, args.stock_unit), Quantity(args.aliquot, args.aliquot_unit),
                    Quantity(args.final_volume, args.volume_unit),
                )
            elif args.command == "infer-concentration":
                result = infer_concentration(json.loads(args.evidence))
            else:
                plan = json.loads(args.plan.read_text(encoding="utf-8"))
                if not isinstance(plan, dict) or set(plan) != {"vessels", "steps"}:
                    raise ValueError("Plan requires vessels and steps.")
                result = simulate_transfers(plan["vessels"], plan["steps"])
            if args.experiment and (
                args.command != "infer-concentration" or result["status"] == "calculated"
            ):
                notebook = LabNotebook(args.db)
                if args.command == "simulate-transfers":
                    sequence = notebook.record_simulation(args.experiment, result)
                else:
                    sequence = notebook.record_calculation(args.experiment, result)
                result = {**result, "record_sequence": sequence}
        print(json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2))
    except (KeyError, OSError, ValueError, ArithmeticError, sqlite3.Error) as exc:
        parser.exit(2, f"zcm: {exc}\n")


if __name__ == "__main__":
    main()
