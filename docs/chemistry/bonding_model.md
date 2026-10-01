# Bonding Knowledge Model

This document defines how SCM should represent and reason about chemical bonding.

## 1. Bonding is an energy/electronic-structure problem

A bond is not merely a line between element symbols. IUPAC describes a chemical bond as a stable interaction between atoms or groups of atoms; ionic, covalent and weaker interactions can all fall under the broad concept. [IUPAC Gold Book](https://goldbook.iupac.org/terms/view/CT07009/pdf)

At the simplest electrostatic level:

- Potential energy: **U(r) = k_e q_1 q_2 / r**
- Force magnitude for point charges: **F(r) = k_e |q_1 q_2| / r²**

These equations describe an electrostatic component, not every chemical bond. Real bonding requires the electronic quantum state, electron-electron repulsion, nuclear repulsion, orbital symmetry, geometry, environment and total-energy change.

A stable two-centre bond normally corresponds to an energetic minimum with respect to internuclear distance:

**dE/dr = 0** at equilibrium, with **d²E/dr² > 0** for a local minimum.

## 2. Main bonding regimes

### Covalent
Electron density is shared between nuclei. A covalent bond is associated with substantial electron density between nuclei and attractive interaction. It is especially useful for molecular structures. [IUPAC](https://goldbook.iupac.org/terms/view/C01384)

### Polar covalent
Still covalent, but electron density is unequal because the atoms have different electron-attracting tendencies. There is no universal hard boundary where a covalent bond suddenly becomes ionic.

### Ionic
Electrostatic attraction between oppositely charged species. Real compounds commonly have mixed ionic/covalent character; IUPAC specifically recommends considering ionic character rather than treating bonds as perfectly pure categories. [IUPAC](https://goldbook.iupac.org/terms/view/IT07058)

Ionic compounds are usually extended lattices rather than collections of isolated NaCl-like molecules. Their properties arise from lattice structure, charge, ion size, hydration/solvation and defects.

### Metallic
Extended electronic states in a metallic solid allow valence electrons to be delocalized through the lattice. This helps explain electrical/thermal conductivity, ductility and metallic cohesion.

### Coordinate/dative
A donor atom supplies an electron pair to an acceptor. The donation origin is a bookkeeping distinction; after formation, the resulting bonding state is described by the same quantum/electronic physics as other bonds.

### Multicentre
Some systems cannot be faithfully represented as independent two-atom bonds. Electron density may stabilize three or more nuclei.

### Hydrogen and halogen bonding
These are directional noncovalent interactions involving electrostatics, polarization, dispersion and charge-transfer/orbital contributions. They should not automatically be assigned ordinary single/double bond orders.

### van der Waals interactions
Weak intermolecular interactions including dispersion and multipolar effects. A common model contains an attractive dispersion term such as **-C6/r^6** plus short-range repulsion.

## 3. Bond order

IUPAC notes that bond order depends on the method used to partition electron density. In molecular-orbital theory a common expression is:

**bond order = (N_bonding - N_antibonding) / 2**

Lewis structures use formal electron-pair counting. These definitions can differ for delocalized systems. [IUPAC](https://goldbook.iupac.org/terms/view/BT07005/pdf)

For closely related bonds between the same atoms, higher bond order commonly correlates with shorter and stronger bonds, but SCM must not convert bond order directly into an invented numerical bond energy.

- single: formal order 1
- double: formal order 2
- triple: formal order 3
- quadruple: possible in specific electronic structures
- aromatic/fractional: effective/delocalized description

A multiple covalent bond can be decomposed conceptually into:
- **sigma (σ):** overlap along the internuclear axis
- **pi (π):** side-on orbital overlap with a nodal plane containing the internuclear axis

This is a model; delocalization can distribute π electron density over several atoms.

## 4. Valence

Valence is not simply "the number of electrons in the outer shell." In practical chemistry it describes combining capacity and bonding relationships, while oxidation state is a formal electron-bookkeeping quantity.

SCM therefore keeps separate:

- valence-electron count
- common valence patterns
- oxidation states
- formal charge
- coordination number
- bond order
- electron configuration
- radical/unpaired-electron state
- actual structural connectivity
- experimental/electronic evidence

The octet rule is a useful model, especially for many second-row main-group compounds, but it has exceptions: odd-electron species, electron-deficient compounds, expanded-valence descriptions, transition-metal chemistry and multicentre bonding.

## 5. Why a bond is possible

SCM should test evidence in layers:

1. **Identity:** What atoms/species are involved?
2. **Electronic state:** What are their electron configurations, charge and spin?
3. **Valence availability:** What common bonding patterns are known?
4. **Orbital compatibility:** Can suitable orbitals interact with the required symmetry?
5. **Electron count:** Can a stable/allowed electronic arrangement be constructed?
6. **Geometry:** Can the atoms approach in a viable orientation and distance?
7. **Electrostatics:** Are attractive and repulsive charge interactions compatible?
8. **Total energy:** Does the proposed structure lower the relevant energy sufficiently to produce a stable state?
9. **Environment:** Solvent, pressure, temperature, crystal field, ligands, surfaces and other surroundings.
10. **Evidence:** Computed, observed, reference or experimental evidence.

A valence rule by itself must never be treated as proof.

## 6. Why a bond may be impossible or unlikely

SCM should distinguish:

- **contradicted:** supplied evidence directly conflicts with the proposed interaction;
- **insufficient data:** the engine cannot establish the interaction;
- **condition-dependent:** the interaction can depend strongly on environment;
- **plausible:** available evidence supports sending it to deeper analysis.

This prevents "not in the periodic-table rule" from being mistaken for a fundamental impossibility.

## 7. Ionic versus covalent compounds

**Ionic compound:** typically an extended arrangement of cations and anions. Important properties include lattice energy, ion size, charge, crystal packing, hydration/solvation, defects and conductivity.

**Molecular covalent compound:** discrete molecular units can dominate, with strong intramolecular bonding and weaker intermolecular interactions. Molecular shape, polarity, hydrogen bonding and dispersion influence macroscopic properties.

**Network covalent material:** atoms form an extended covalent network, so treating it like an ordinary molecular compound is inappropriate.

**Metallic solid:** extended electronic states produce properties very different from either a molecular covalent solid or ionic lattice.

These categories are structural models, not mutually exclusive boxes of nature.

## 8. Cross-domain consequences

Bonding information feeds directly into:

- **Physics:** energy surfaces, forces, quantum states, spectra, band structure.
- **Chemistry:** structure, reactivity, equilibrium, kinetics, acid-base and redox behavior.
- **Biology:** protein folding, nucleic-acid pairing, ligand recognition, membranes.
- **Medicine:** drug-target interactions, coordination complexes, analytical assays, formulation and biomolecular structure.
- **Materials:** conductivity, hardness, elasticity, corrosion, catalysis, semiconductors.
- **Industrial chemistry:** catalysts, reaction selectivity, polymers, separation, corrosion, formulation and process conditions.
- **Laboratory science:** qualitative identification, spectroscopy, precipitation, titration and sample interpretation.

The computational rule remains: **bonding knowledge supplies constraints and explanations; electronic/energetic calculations and evidence establish the actual result.**
