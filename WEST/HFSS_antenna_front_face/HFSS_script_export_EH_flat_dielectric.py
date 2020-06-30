# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0
# 10:18:37  mai 20, 2020
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("WEST_ICRH_front_face")
oDesign = oProject.SetActiveDesign("Front Face Flat Dielectric")

N=10000

oModule = oDesign.GetModule("FieldsReporter")
oModule.ChangeGeomSettings(N)


oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Real_vector_E")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_Ereal.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	])

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_E")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_Eimag.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	])

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Real_vector_H")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_Hreal.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	])

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_H")
oModule.EnterLine("vacuum_line_toroidal")
oModule.CalcOp("Value")
oModule.CalculatorWrite("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_Himag.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	])

