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

LCM is the language-facing layer. It translates English questions and instructions into structured operations on SCM and converts SCM results into explanations that humans can understand. English is the only supported natural language for the current project scope. LCM should not replace the scientific model; it should communicate with it.

## Scientific Representation

A chemical property must not always be represented as a single number. A property may depend on temperature, pressure, composition, phase, purity, concentration, electronic state, crystal structure, solvent, measurement method, and experimental conditions.

Therefore SCM should represent properties conceptually as:

Property + Value + Unit + Conditions + Evidence + Uncertainty

Examples include melting/freezing/boiling points, sublimation point, critical temperature and pressure, density, heat capacity, enthalpies of phase change, ionization energies, electron affinity, electronegativity, atomic and ionic radii, conductivity, solubility, viscosity, vapour pressure, and spectroscopic and magnetic properties.

## Physical Meaning and Causal Reasoning

SCM should attempt to represent why a property has a particular value rather than only storing it. Periodic trends may relate to nuclear charge, electron configuration, effective nuclear charge, shielding, orbital structure, electron-electron interactions, atomic size, bonding, intermolecular forces, crystal structure, and thermodynamic state. Trends are not absolute rules: scientifically established exceptions and their explanations must remain representable.

## Phase Transitions

SCM should represent phase transitions as relationships between states. For a pure substance at specified pressure and equilibrium conditions, melting and freezing describe the same solid-liquid phase-equilibrium temperature. Observed behaviour may differ because of supercooling, superheating, impurities, mixtures, nucleation barriers, or experimental conditions. SCM must distinguish equilibrium properties from observed experimental transition behaviour.

## Complete Element Knowledge

SCM is intended to represent all officially recognized chemical elements and their relevant scientific information. Elements should be accessible by atomic number, periodic-table position, group, period, block, electron configuration, chemical classification, atomic structure, properties, periodic trends, oxidation states, common ions, bonding behaviour, reactivity, isotopes, energetics, and experimental evidence. The same element should be accessible from multiple scientific perspectives without duplicating its underlying identity.

## Exceptions and Scientific Reasoning

SCM should distinguish general trend, underlying physical reason, expected behaviour, observed behaviour, exception, explanation, confidence, and supporting evidence. It must not force every observation into a simplified rule.

## Knowledge and Evidence

SCM should distinguish:

- **Known** — supported by reliable scientific evidence
- **Observed** — directly represented experimental observation
- **Calculated** — derived through a defined mathematical or physical model
- **Predicted** — model-based inference with uncertainty
- **Hypothesized** — proposed explanation requiring validation

Scientific claims should retain provenance whenever practical.

## Chemical State

Chemistry is represented as evolving states rather than only equations. A chemical state may contain species, quantities, concentrations, temperature, pressure, volume, phase distribution, energy, pH, solvent, impurities, reaction progress, environmental conditions, and uncertainty.

Processes may therefore be represented as:

STATE₀ → INTERACTIONS → INTERMEDIATE STATES → STATE₁

## Reaction and Process Intelligence

SCM is intended to reason about stoichiometry, electron transfer, bond changes, energy changes, reaction pathways, kinetics, equilibrium, side reactions, conversion, selectivity, yield, purity, separation, purification, material balances, energy balances, and process conditions.

Potential application areas include soap and detergents, food and beverages, fermentation, cosmetics, cleaning chemistry, pharmaceutical chemistry, dyes and pigments, polymers, materials, water treatment, agricultural chemistry, and industrial chemical processes. Proprietary commercial formulations must never be presented as known facts without appropriate evidence.

## Visualization and Sensorium

SCM should eventually generate structured visualization for molecules, atoms, bonds, molecular geometry, reactions, laboratory apparatus, industrial equipment, process flows, and phase behaviour. Visualization should be generated from structured scientific representations rather than treated only as decorative imagery.

Computational sensor channels may represent measurable properties such as colour, opacity, spectral behaviour, temperature, pressure, viscosity, density, conductivity, pH, chemical signatures, and mechanical or acoustic process signals. These are representations of measurable phenomena, not literal biological senses.

## Production Testing

SCM must be evaluated as a real software system. Testing should include unit tests, scientific validation, mathematical consistency, integration tests, simulation tests, benchmark questions, experimental-data comparison, exception-reasoning tests, real-world chemistry tasks, and production application testing.

The same scientific kernel should eventually support command-line, web, desktop, Android, and other interfaces.

## Development Principles

1. Scientific evidence comes before unsupported claims.
2. Calculated, observed, predicted, and hypothesized results remain distinguishable.
3. Conditions accompany properties whenever they materially affect results.
4. Exceptions are represented rather than hidden.
5. Units and dimensional consistency are mandatory.
6. Conservation laws must be testable.
7. Knowledge, scientific models, software logic, and experimental evidence remain separable.
8. Core scientific functionality must not depend on external AI APIs.
9. Heavy computation should scale to more powerful hardware.
10. The system must remain portable between mobile development, cloud development, and PCs.
11. English is the sole natural-language interface in the current scope.

## Development Status

SCM-0001 — Project Foundation. The repository now contains executable scientific foundations beyond the initial scaffold, but domain completeness and experimental validation remain ongoing work.

Initial dependency order:

1. Project foundation and shared validation
2. Element and periodic-table model
3. Atomic, isotope, electron, and ion models
4. Chemical identity and nomenclature
5. Bonding and molecular structure
6. Chemical state and units
7. Stoichiometry and conservation
8. Condition-aware properties and provenance
9. Reaction plausibility and mechanisms
10. Thermodynamics, kinetics, and equilibrium
11. Analytical chemistry and uncertainty
12. Laboratory apparatus and practical workflows
13. Pharmaceutical, medical-laboratory, and industrial domain models
14. Research data, experiments, and provenance
15. Visualization and sensorium
16. LCM English intent parsing and explanations
17. ZCM service API, Python SDK, and CLI
18. Scientific benchmarks and integration testing
19. Education, laboratory, research, pharma/medical, and industrial products
20. Instrument and robotics interfaces

This project is experimental scientific software and research. Model predictions must not be treated as experimentally validated facts without appropriate evidence.

## Current Kernel Expansion

Current repository foundations include conservative oxidation-state assignment with explicit ambiguity; stoichiometric limiting-reagent calculations; thermodynamic bookkeeping; Arrhenius and rate-law primitives; reaction-quotient/equilibrium calculations; analytical dilution, Beer-Lambert, calibration, pH, and titration calculations; explicit reaction-mechanism bond/electron-pair edit records; coordination-chemistry records; canonical chemical identity keys; atom/ion electron-state consistency validation; research experiments and dataset provenance records; structured molecular/laboratory/process/sensor visualization scenes; apparatus and measurement records; a ZCM service facade, Python SDK and CLI entry point; education, laboratory, research and industrial workspace surfaces; and formulation/process-engineering data models.

These are computational foundations, not claims that every scientific domain is complete or experimentally validated. Missing scientific data must remain explicit rather than fabricated.
