# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0
# 12:48:39  mai 20, 2020
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("WEST_ICRH_front_face")
oDesign = oProject.SetActiveDesign("Front Face Flat Dielectric")
oModule = oDesign.GetModule("FieldsReporter")

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Real_vector_E")
oModule.ExportToFile("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_2D_Ereal.fld", "C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\points.pts", "Setup1 : LastAdaptive", 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	], True)

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Real_vector_H")
oModule.ExportToFile("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_2D_Hreal.fld", "C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\points.pts", "Setup1 : LastAdaptive", 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	], True)

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_E")
oModule.ExportToFile("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_2D_Eimag.fld", "C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\points.pts", "Setup1 : LastAdaptive", 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	], True)

oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Imag_vector_H")
oModule.ExportToFile("C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\WEST_ICRH_Flat_Dielectric_2D_Himag.fld", "C:\\Users\\JH218595\\Documents\\ICRH\\WEST\\HFSS_antenna_front_face\\points.pts", "Setup1 : LastAdaptive", 
	[
		"$epsr_dielectric:="	, "1",
		"$shift_X:="		, "50mm",
		"Freq:="		, "0.05GHz",
		"Phase:="		, "0deg",
		"power_at_port:="	, "1000W",
		"vac_length:="		, "200mm",
		"vac_width:="		, "1200mm",
		"x0:="			, "5mm"
	], True)