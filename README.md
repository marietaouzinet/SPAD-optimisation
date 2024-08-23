# SPAD-optimisation

## Introduction
As part of my engineering studies at Telecom Physique Strasbourg, I'm doing a 3-month internship at VTEC Lasers and sensors in Eindhoven, the Netherlands. As I specialise in quantum science and technology, my internship subject is single-photon detector technology, which is useful in the field of quantum photonics.

Single-photon detectors for the near-infrared wavelength region, such as single-photon
avalanche diodes (SPADs), are receiving increasing interest in a growing number
of photon counting applications, including, for example, quantum cryptography and computing, 3-D laser ranging (LIDAR), time-resolved spectroscopy, etc. InGaAs/InP SPADs are used for single-photon counting and photon timing, typically at 1550 nm.

## Goals
The aim is to simulate and then optimise, the efficiency of a SPAD detector. This optimisation involves calculating the photodetection efficiency (PDE) and the dark count rate (DCR).

## Project architecture
The project is divided into three parts:
- A section for simulating the PDE. This parameter depends on the avalanche triggering Pbd and photon absorption probabilities QE. The Pbd probability was found thanks to the Runge Kutta 4 numerical method capable of solving coupled and non-linear differential equations. To make it easier to visualise the results and modify the parameters influencing the Pbd and QE probability values, I implemented a graphical interface using tkinter. This section has been implemented in the ‘Modelling’ folder.
- A section for simulating the DCR, created by another intern.
- A section for optimising the total efficiency of the single-photon diode by increasing the PDE and decreasing the DCR as much as possible. These two parameters depend on the thickness and doping concentration of the various semiconductor layers making up the SPAD. Optimisation will therefore involve adjusting the thicknesses and concentrations to achieve the best performance. This section has been implemented in the ‘Optimisation’ folder. Two techniques are implemented here, but it was not possible to test either of them.

## Paper
For more details, please see my paper：
