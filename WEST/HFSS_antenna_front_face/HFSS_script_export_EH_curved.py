# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0
# 18:20:45  mai 08, 2020
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("WEST_ICRH_front_face")
oDesign = oProject.SetActiveDesign("Front Face Curved")
oModule = oDesign.GetModule("FieldsReporter")
oModule.CalcStack("clear")
oModule.ChangeGeomSettings(10000)
oModule.CopyNamedExprToStack("Real_vector_E")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Curved_Vacuum_Ereal.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg"
	])
oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_E")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Curved_Vacuum_Eimag.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg"
	])
oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Real_vector_H")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Curved_Vacuum_Hreal.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg"
	])
oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_H")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Curved_Vacuum_Himag.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg"
	])
