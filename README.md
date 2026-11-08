# ZamCan Software Chemistry

ZamCan Software Chemistry is a scientific software research project for building a computational model of chemistry.

The central objective is to develop a Software Chemistry Model (SCM) that represents chemical entities, physical and chemical properties, interactions, transformations, processes, observations, evidence, uncertainty, and scientific relationships as computational structures.

## Core Systems

### SCM — Software Chemistry Model

SCM is the computational chemical world model.

It is intended to represent:

- Elements
- Atoms
- Nuclei
- Electrons
- Electron configurations
- Ions
- Isotopes
- Bonds
- Molecules
- Molecular structures
- Materials
- Chemical states
- Phases
- Reactions
- Reaction mechanisms
- Thermodynamics
- Kinetics
- Equilibrium
- Energy
- Chemical and physical properties
- Laboratory processes
- Industrial processes
- Experimental observations
- Scientific evidence
- Uncertainty
- Predictions
- Chemical visualization

SCM should not treat chemistry as a collection of disconnected facts. Properties and behaviours should be connected to underlying structure, conditions, mechanisms, measurements, and evidence wherever scientifically justified.

### LCM — Language Chemistry Model

LCM is the language-facing layer.

It translates human questions and instructions into structured operations on SCM and converts SCM results into explanations that humans can understand.

LCM should not replace the scientific model. It should communicate with it.

## Scientific Representation

A chemical property must not always be represented as a single number.

A property may depend on:

- Temperature
- Pressure
- Composition
- Phase
- Purity
- Concentration
- Electronic state
- Crystal structure
- Solvent
- Measurement method
- Experimental conditions

Therefore SCM should represent properties conceptually as:

Property + Value + Unit + Conditions + Evidence + Uncertainty

Examples include:

- Melting point
- Freezing point
- Boiling point
- Sublimation point
- Critical temperature
- Critical pressure
- Density
- Heat capacity
- Enthalpy of fusion
- Enthalpy of vaporization
- Ionization energies
- Electron affinity
- Electronegativity
- Atomic radius
- Ionic radius
- Conductivity
- Solubility
- Viscosity
- Vapour pressure
- Spectroscopic properties
- Magnetic properties

## Physical Meaning and Causal Reasoning

SCM should attempt to represent why a property has a particular value rather than only storing the value.

For example, periodic trends may be related to:

- Nuclear charge
- Electron configuration
- Effective nuclear charge
- Shielding
- Orbital structure
- Electron-electron interactions
- Atomic size
- Bonding
- Intermolecular forces
- Crystal structure
- Thermodynamic state

Trends are not automatically treated as absolute rules. SCM must be able to represent scientifically established exceptions and explain why observed behaviour differs from a simplified periodic trend.

## Phase Transitions

SCM should represent phase transitions as relationships between states.

For a pure substance at specified pressure and equilibrium conditions, melting and freezing describe the same solid-liquid phase-equilibrium temperature.

Observed behaviour may differ because of effects such as:

- Supercooling
- Superheating
- Impurities
- Mixtures
- Nucleation barriers
- Experimental conditions

SCM must therefore distinguish thermodynamic equilibrium properties from observed experimental transition behaviour.

## Complete Element Knowledge

SCM is intended to represent all officially recognized chemical elements and their relevant scientific information.

Elements should be accessible through multiple scientifically meaningful organizations, including:

- Atomic number
- Periodic table position
- Group
- Period
- Block
- Electron configuration
- Chemical classification
- Atomic structure
- Physical properties
- Chemical properties
- Periodic trends
- Oxidation states
- Common ions
- Bonding behaviour
- Reactivity
- Isotopes
- Energetics
- Experimental evidence

The same element should therefore be accessible from many different scientific perspectives without duplicating its underlying identity.

## Exceptions and Scientific Reasoning

A central SCM capability is reasoning about exceptions.

SCM should be able to distinguish:

- General trend
- Underlying physical reason
- Expected behaviour
- Observed behaviour
- Exception
- Explanation for the exception
- Confidence
- Supporting evidence

The goal is not to force every observation into a simplified rule.

## Knowledge and Evidence

SCM should distinguish:

- Known — supported by reliable scientific evidence
- Observed — directly represented experimental observation
- Calculated — derived through a defined mathematical or physical model
- Predicted — model-based inference with uncertainty
- Hypothesized — proposed explanation requiring validation

Scientific claims should retain their provenance whenever practical.

## Chemical State

Chemistry is represented as evolving states rather than only equations.

A chemical state may contain:

- Species
- Quantities
- Concentrations
- Temperature
- Pressure
- Volume
- Phase distribution
- Energy
- pH
- Solvent
- Impurities
- Reaction progress
- Environmental conditions
- Uncertainty

Processes may therefore be represented as:

STATE₀ → INTERACTIONS → INTERMEDIATE STATES → STATE₁

## Reaction and Process Intelligence

SCM is intended to reason about:

- Stoichiometry
- Electron transfer
- Bond changes
- Energy changes
- Reaction pathways
- Kinetics
- Equilibrium
- Side reactions
- Conversion
- Selectivity
- Yield
- Purity
- Separation
- Purification
- Material balances
- Energy balances
- Process conditions

Industrial and laboratory chemistry may eventually include:

- Soap and detergents
- Food and beverages
- Fermentation
- Cosmetics
- Cleaning chemistry
- Pharmaceutical chemistry
- Dyes and pigments
- Polymers
- Materials
- Water treatment
- Agricultural chemistry
- Industrial chemical processes

Proprietary commercial formulations must never be presented as known facts without appropriate evidence.

## Visualization

SCM should eventually have native structured visualization capabilities for:

- Molecules
- Atoms
- Bonds
- Molecular geometry
- Chemical reactions
- Laboratory apparatus
- Industrial equipment
- Process flows
- Phase behaviour
- Scientific diagrams

Visualization should be generated from structured scientific representations rather than being treated only as decorative imagery.

## Sensorium

SCM may eventually expose computational sensor channels representing measurable properties such as:

- Visual appearance
- Colour
- Opacity
- Spectral behaviour
- Temperature
- Pressure
- Viscosity
- Density
- Conductivity
- pH
- Chemical signatures
- Mechanical or acoustic process signals

These are computational representations of measurable phenomena, not literal biological senses.

## Production Testing

SCM must eventually be evaluated as a real software system, not only as source code.

Testing will include:

1. Unit tests
2. Scientific validation tests
3. Mathematical consistency tests
4. Integration tests
5. Simulation tests
6. Benchmark questions
7. Experimental-data comparison
8. Exception-reasoning tests
9. Real-world chemistry tasks
10. Production application testing

The same scientific kernel should eventually support:

- Command-line applications
- Web applications
- Desktop applications
- Android applications
- Other interfaces

The objective is to measure SCM capabilities quantitatively rather than merely claiming that it is intelligent.

## Development Principles

1. Scientific evidence comes before unsupported claims.
2. Calculated, observed, predicted, and hypothesized results remain distinguishable.
3. Conditions must accompany properties whenever they materially affect the result.
4. Exceptions must be represented rather than hidden.
5. Units and dimensional consistency are mandatory.
6. Conservation laws must be testable.
7. Knowledge, scientific models, software logic, and experimental evidence remain separable.
8. Core scientific functionality should not depend on external AI APIs.
9. Heavy computation should remain scalable to more powerful hardware.
10. The system must remain portable between mobile development, cloud development, and PCs.

## Development Status

SCM-0001 — Project Foundation

The repository architecture is being established before implementing the scientific kernel.

Initial development sequence:

1. Project foundation
2. Element model
3. Periodic table
4. Atomic model
5. Electron model
6. Ion model
7. Bond model
8. Molecular structure
9. Chemical state
10. Reaction engine
11. Energy and thermodynamics
12. Kinetics
13. Equilibrium
14. Properties
15. Prediction and uncertainty
16. Process modeling
17. Visualization
18. LCM integration
19. Scientific benchmarks
20. Production applications

This project is experimental scientific software and research. Model predictions must not be treated as experimentally validated facts without appropriate evidence.

## Current Kernel Expansion

The repository contains executable foundations beyond the original project scaffold. LCM and documentation are English-only. Current capabilities include:

- conservative oxidation-state assignment with explicit ambiguity
- stoichiometric limiting-reagent calculations
- Gibbs free-energy and thermodynamic bookkeeping
- Arrhenius/rate-law kinetics calculations
- reaction-quotient/equilibrium calculation primitives
- analytical titration calculations
- explicit reaction-mechanism bond/electron-pair edit records
- coordination-chemistry ligand/coordination-number records
- canonical chemical identity keys
- atom/ion electron-state consistency validation
- multilingual English/Swahili/Arabic chemistry vocabulary
- research experiments and dataset provenance records
- structured Nano/Molecular/Laboratory/Process/Sensor visualization scenes
- laboratory apparatus/measurement records
- ZCM chemistry service facade, Python SDK and CLI entry point
- shared education, laboratory, research and industrial workspace surfaces
- formulation and process-engineering data models

These are computational foundations, not claims that every scientific domain is already experimentally validated. Missing scientific data remains explicit rather than fabricated.

## Offline calculator, laboratory notebook, and robotics simulation

Install with Python 3.11 or later. The runtime uses the standard library.

```sh
python -m pip install .
zcm calculate 'molar mass Ca(OH)2'
zcm calculate 'balance equation H2 + O2 -> H2O'
zcm stoichiometry 'H2 + O2 -> H2O' '{"H2":"0.30","O2":"0.20"}'
zcm titrate 0.100 25.00 20.00 --ratio 1
zcm titrate 0.100 25.00 20.00 --equation 'NaOH + H2SO4 -> Na2SO4 + H2O' --titrant NaOH --analyte H2SO4
zcm molarity 25 500 --amount-unit mmol
zcm mass-molarity NaCl 5.844 1 --volume-unit L
zcm dilute 1 25 250
```

The calculator returns JSON. Molar mass uses the offline [CIAAW 2024 standard
atomic weights](https://ciaaw.org/atomic-weights.htm) for 84 elements. It retains
natural-composition intervals and reports tabulated uncertainty per element.
Elements without a standard atomic weight produce an explicit error.
Stoichiometry reports theoretical yields and limiting
reactants using exact fractions in mol. The titration inputs are titrant
concentration in mol/L and both volumes in mL. The ratio is analyte moles per
titrant mole at equivalence. An equation with two reactants can supply that
ratio through the balanced coefficients. This calculates an equivalence
result for the supplied reaction and measurements. Formula input supports neutral formulas and
parenthesized groups. Ionic and hydrate notation are outside the CLI syntax.

Molarity uses the **final solution volume**, defaulting to mL. Mass-based
molarity calculates moles from the formula and pure solute mass, and
preserves the molar-mass interval when present. Dilution takes stock
concentration, aliquot volume, and final solution volume in that order.
All three commands accept `--experiment` to store the inputs and result.

### Record and analyze a practical

```sh
zcm --db practical.sqlite3 lab create 'Titration' 'Compare replicate titres'
# Set experiment to the experiment_id returned by the create command.
zcm --db practical.sqlite3 lab measure "$experiment" titre 24.95 mL --instrument B-01 --uncertainty 0.05
zcm --db practical.sqlite3 lab measure "$experiment" titre 25.05 mL --instrument B-01 --uncertainty 0.05
zcm --db practical.sqlite3 lab note "$experiment" 'Endpoint readings recorded.'
zcm --db practical.sqlite3 lab dataset "$experiment" log-01 v1 'Bench notes' 'Lab notebook 01'
zcm --db practical.sqlite3 lab summarize "$experiment" titre mL --save
zcm --db practical.sqlite3 titrate 0.100 25.00 20.00 --experiment "$experiment"
zcm --db practical.sqlite3 lab export "$experiment" > practical.json
```

The SQLite notebook preserves ordered measurements, notes, dataset provenance,
calculations, and simulations. Replicate summaries select an exact quantity
and unit and retain the measurement sequence IDs. The summary reports sample
dispersion independently of each instrument's recorded uncertainty.

### Simulate a robotics transfer plan

Save this as `plan.json` and run `zcm simulate-transfers plan.json`. To save
the trace in a practical, pass `--db practical.sqlite3` before
`simulate-transfers` and `--experiment "$experiment"` after the filename.

```json
{
  "vessels": {
    "stock": {"capacity_ul": 1000, "volume_ul": 800},
    "sample": {"capacity_ul": 500, "volume_ul": 0}
  },
  "steps": [{"source": "stock", "destination": "sample", "volume_ul": 250}]
}
```

The simulator models volume accounting in integer microliters. Hardware
actuation and device commissioning are separate from this workflow. The
calculator, notebook, and simulator are also available through
`zcm.sdk.ZCMClient`. LCM uses deterministic language patterns for its supported
queries. It does not require a hosted model.

### Infer a concentration calculation from evidence

The SCM analytical planner selects a method from the fields provided. It
returns the candidate methods and missing evidence when the inputs are
incomplete, and flags fields from incompatible methods. A completed trace
includes the chosen method, the evidence used, and the calculation.

```sh
zcm infer-concentration '{"amount":{"value":25,"unit":"mmol"},"final_volume":{"value":500,"unit":"mL"}}'
zcm infer-concentration '{"titrant_mol_l":0.100,"titrant_ml":25.00,"analyte_ml":20.00}'
```

The second request asks for an explicit mole ratio or the equation and
reactant formulas. Add `--experiment` to save a completed trace to a lab
record. Python callers can use `ZCMClient().infer_concentration(evidence)`.

### Interpret an unknown single salt

Use `zcm lab ion-tests` to see supported test and outcome identifiers.
Record observations already made under the referenced test conditions, and
analyze one sample at a time within a practical:

```sh
zcm --db practical.sqlite3 lab observe-ion "$experiment" sample-a flame yellow
zcm --db practical.sqlite3 lab observe-ion "$experiment" sample-a silver_nitrate_nitric_acid white_precipitate
zcm --db practical.sqlite3 lab identify-salt "$experiment" sample-a --save
```

The result lists candidate ions and points to the supporting notebook
entries. A unique supported pair yields a charge-balanced formula
hypothesis. Ambiguous, conflicting, and insufficient evidence remain
separate outcomes. The catalogue covers a limited set of positive
signatures in the referenced educational syllabus. Mixtures, unlisted ions,
purity, and hydration state are outside this model. Recorded tests with no
observable change do not establish that an ion is absent. Python callers
can pass `Observation` objects to `ZCMClient().identify_salt`.
