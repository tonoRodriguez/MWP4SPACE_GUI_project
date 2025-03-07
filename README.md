# Python Code for Fast PIC Component Design and PDK Design

This project starts as a compilation of all the designs I am making during my industrial PhD. It compiles several technologies that I needed to test. The idea of this project is to have a tool that allows users, whether familiar or not with Lumerical, to design fast and simple components using proven templates. This will allow participation in MWP even if there is not much time to design.

## Technologies Available

### AL2O3
For participating in the Alubia run.

### LNOI_CG
PDK for participating in the LNOI run with CamGraphics. It's a rib waveguide as shown below:

<p align="center">
  <img src="https://github.com/user-attachments/assets/8352590d-0671-44fe-aad5-15bb7db6b24d" alt="LNOI" width="300">
</p>

#### Specifications:
- **h_f** = 600 nm
- **h_e** = 300 nm
- **θ** = between 65° and 75°
- **SiO₂** = 3 µm
- **Outside Cladding** = Not defined yet

## Files and Folders

### General Structure

Files and Folders:
	- /Interconnect: Folder created to save the S parameter tha can be created using the scripts
	-/Material_script/LNOI_materials: Lumerical Script with the definition of several Materials including AlO2, Lithium Niobate, Si, Silica between others using the Sellmier equations.
 
### Python Scripts

#### `Data_Structure.py`
Defines an object to handle the results obtained from Lumerical.

#### `Mode_analysis.py`
Performs basic measurements of waveguide minimum width and minimum bend, as well as dispersion analysis.

**Main Functions:**
- `mode_analysis`: Single FDE simulation.
- `rad_analysis`: Iterative radius analysis for different offsets.

**Status:** In progress.

#### `PDK_GUI.py`
Uses Tkinter to call functions from `Mode_analysis.py`.

**Status:** Missing single calculation visibility in mode analysis. Needs name update.

#### `plot_Data.py`
Used for plotting data obtained from mode analysis.

**Main Functions:**
- `Analyse_ng_disspersion`: Uses the effective index for multiple frequencies.
- `plot_excel_sheet`: Plots values against waveguide width.

**Status:** Needs an easier interface. Requires checking for bend analysis.

#### `ring_resonator.py`
Simulates ring resonators and writes the information to a Word document.

**Status:** Needs update. Improve 2-branch ring resonator simulation.

#### `Ring_Resonator_GUI.py`
Uses Tkinter to call `ring_resonator.py`.

**Status:** Needs update.

#### `SSC_Analysis.py`
Simulates tapers and MMIs, allowing different architectures to be combined.

**Main Functions:**
- `SSC_sim`: Simulates tapers.
- `mmi_sim`: Simulates an MMI.

**Status:** Needs update and renaming.

#### `SSC_GUI.py`
Uses Tkinter to call `SSC_Analysis.py`.

**Status:** Finished.

#### `Y_spl_Power_Coupler.py`
Simulates a Y Splitter/Combiner and a Power Coupler.

**Main Functions:**
- `y_splitter`: Creates a Y splitter/combiner.
- `PowerCoupler`: Creates a directional coupler.

**Status:** Not extensively tested.

#### `YS_PC_GUI.py`
Uses Tkinter to call `Y_spl_Power_Coupler.py`.

**Status:** Finished.

---

## SiN
Code for participating in the Cornerstone/Akethonics student batch.

## SOI_Cornerstone
PDK for participating in the SOI student batch of Cornerstone. It's a rib waveguide with the following specifications:

<p align="center">
  <img src="https://github.com/user-attachments/assets/b82fa280-c752-4632-af77-058c8031b12a" alt="SOI">
</p>

## Additional Files and Folders


	- /Interconnect: Folder created to save the S parameter tha can be created using the scripts
	-/Material_script/LNOI_materials: Lumerical Script with the definition of several Materials including AlO2, Lithium Niobate, Si, Silica between others using the Sellmier equations.
	-Data_Structure.py: Python script defining an object that allows me to work with the results obtained from Lumerical
	-Mode_analysis.py: Python Script for obtaining basic measurements regarding the waveguide min width and minimum bend, It also gives you information 
			regarding dispertion and 
		-Main Functions: mode_analysis (Single FDE simulation), rad_analysis (itterative radious analysis to get different offcets)
		-Status: In Progress.
	-PDK_GUI.py:This Script uses tkinter to call the functions from Mode_analysis as its shown in the following figure.
		-Status: Missing single calculation visibility in Made analysis. Missing name change to 
	-plot_Data.py: Script used for plotting the data obtained after runing Mode analysis.
		-Main Functions: Analyse_ng_disspersion (uses the effective index for multiple frequencies), plot_excel_sheet (plots the values with respect to the waveguide width)
		-Status: Misiing an easier way to use it, Needs to be checked for the bend analysis.
	-ring_resonator.py: Script used to simulate ring resonators. Single function that simulates and write the infromation of a ring resonator in a word document.
		-Status: Needs update, improve 2 branch ring resonator
	-Ring_Resonator_GUI.py: This Script uses tkinter to call the functions from ring_resonator.py. Straight forward to use.
		-Status: Needs update
	-SSC_Analysis.py:  This Script is used to simulate tappers and MMIs. The goal is to be able to combine multiple tappers and MMIs architectures.
		-Main functions: SSC_sim (Simulates tappers), mmi_sim (Simulates an MMi)
		-Status:Needs update, change of name
	-SSC_GUI.py: This Script uses tkinter to call the functions from SSC_Analysis.py
		-Status: Finished
	-Y_spl_Power_Coupler.py: This script is used to simulate a Y Splitter/Combiner and a Power Coupler.
		-Main functions: y_splitter (Creates a Y splitter/ Combiner), PowerCoupler (Creates a directional coupler)
		-Status: Not extensibly tested
	-YS_PC_GUI.py: This Script uses tkinter to call the function Y_spl_Power_Coupler.py.
		-Status: Finished
