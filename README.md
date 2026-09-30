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
