Pyhton code for fast PIC component design and fast PDK design

This project starts as a compilation of all the design I am makingduring my industrial PhD. I compiles several technologies that I needed to test. The idea of this project is to have a tool that allows users that are and aren't familiar with Lumerical design fast simple componets with templates that were already proven. This will allow to
participate in MWP even if theres not much time to design.

Technologies available:

- AL2O3 for participating in the Alubia run

- LNOI_CG: PDK for participating in the LNOI run with CamGraphics: It's a rib waveguide as the following:

<p align="center">
  <img src="https://github.com/user-attachments/assets/8352590d-0671-44fe-aad5-15bb7db6b24d" alt="LNOI" width="300">
</p>

Where: 
	hf = 600 nm
	he = 300 nm
	θ = between 65 and 75 degrees
	SiO2 = 3um
	Outside Cladding = Not defined yet
Files and Folders:
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

- SiN: Code for participaten in the Cornerstone/Akethonics student batch
- SOI_Cornerstone: PDK for participating in the SOI student batch of Cornerstone: It's a rib waveguide with the following specifications:
![image](https://github.com/user-attachments/assets/b82fa280-c752-4632-af77-058c8031b12a)

