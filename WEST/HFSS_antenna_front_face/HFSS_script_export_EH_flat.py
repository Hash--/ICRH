# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0
# 19:05:23  mai 08, 2020
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("WEST_ICRH_front_face")
oDesign = oProject.SetActiveDesign("Front Face Flat")
N=10000

oModule = oDesign.GetModule("FieldsReporter")
oModule.ChangeGeomSettings(N)


oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Real_vector_E")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Vacuum_Ereal.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"vac_width:="		, "1200mm",
		"x0:="			, "2mm"
	])

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_E")
oModule.EnterLine("vacuum_line_toroidal")
# oModule.ClcEval("Setup1 : LastAdaptive", 
# 	[
# 		"Freq:="		, "0.05GHz",
# 		"Phase:="		, "0deg",
# 		"vac_width:="		, "1200mm",
# 		"x0:="			, "2mm"
# 	])
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Vacuum_Eimag.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"vac_width:="		, "1200mm",
		"x0:="			, "2mm"
	])

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Real_vector_H")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Vacuum_Hreal.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"vac_width:="		, "1200mm",
		"x0:="			, "2mm"
	])

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_H")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Vacuum_Himag.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"vac_width:="		, "1200mm",
		"x0:="			, "2mm"
	])
