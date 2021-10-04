from PySide2.QtGui import QDoubleValidator, QIntValidator

################################# APP PROPERTIES #################################



TITLE								=	"Correção de Corrente"				# Title of application

ICON_PATH							=	"icons/window/512x512"				# Icon of application

WIDTH								=	1280								# Width of application
HEIGHT								=	800									# Height of application

MAX_WIDTH_DIALOG					=	200									# Maximum Width of Dialog

#BACKGROUND_STYLESHEET				=	"background-color: #595959;"		# Background color of application black
BACKGROUND_STYLESHEET				=	""#"background-color: white;"			# Background color of application white


TOP_MARGIN							=	20									# Margin do the top of application
BOTTOM_MARGIN						=	20									# Margin do the bottom of application
LEFT_MARGIN							=	20									# Margin do the left of application
RIGHT_MARGIN						=	10									# Margin do the right of application


MATPLOTLIB_TOOLBAR_STYLESHEET		=	""#"background-color: gray;"			# Stylesheet for matplotlib's toolbar


GUI_UPDATE_TIME						=	1000								# Interval between updates in the GUI in miliseconds



############################### BUTTONS PROPERTIES ###############################



CONFIG_BUTTON_ICON					=	"icons/config/512x512"				# Icon of the configuration tab
CONFIG_BUTTON_SIZE					=	35									# Size of the configuration tab button
CONFIG_BUTTON_STYLESHEET			= 	"background-color: green; font-size: 16px; font-family: Arial; font-weight: 600; color: white;"
																			# Stylesheet for the config button

SAVE_BUTTON_TEXT					=	"SAVE"								# Text of the configuration save button
SAVE_BUTTON_SIZE					=	40									# Size of the configuration save button
SAVE_BUTTON_STYLESHEET				= 	"background-color: green; font-size: 16px; font-family: Arial; font-weight: 600; color: white;"
																			# Stylesheet for the save button

CSVS_PLOT_BUTTON_TEXT				=	"PLOT CSV's"						# Text of the current curve button
CSVS_PLOT_BUTTON_HEIGHT				=	40									# Size of the current curve button
CSVS_PLOT_BUTTON_STYLESHEET			= 	"background-color: green; font-size: 16px; font-family: Arial; font-weight: 600; color: white;"
																			# Stylesheet for the current curve button

CURVE_CURRENT_BUTTON_TEXT			=	"GET CURRENT CURVE"					# Text of the current curve button
CURVE_CURRENT_BUTTON_HEIGHT			=	40									# Size of the current curve button
CURVE_CURRENT_BUTTON_STYLESHEET		= 	"background-color: green; font-size: 16px; font-family: Arial; font-weight: 600; color: white;"
																			# Stylesheet for the current curve button

CURVE_CORRECTION_BUTTON_TEXT		=	"RUN SIMULATED ANNEALING"			# Text of the current correction button
CURVE_CORRECTION_BUTTON_HEIGHT		=	40									# Size of the current correction button
CURVE_CORRECTION_BUTTON_STYLESHEET	= 	"background-color: green; font-size: 16px; font-family: Arial; font-weight: 600; color: white;"
																			# Stylesheet for the current correction button

CSV_BUTTON_TEXT						=	"OPEN CSV"							# Text of a button to open an csv file
CSV_OPENED_BUTTON_TEXT				=	"CSV OPENED"						# Text of a button when an csv file is opened
CSV_BUTTON_HEIGHT					=	30									# Size of a button to open an csv file
CSV_BUTTON_STYLESHEET				= 	"background-color: green; font-size: 16px; font-family: Arial; font-weight: 600; color: white;"
																			# Stylesheet foe a button to open an csv file

CLOSE_BUTTON_STYLESHEET				= 	"background-color: green; font-size: 16px; font-family: Arial; font-weight: 600; color: white;"
																			# Stylesheet for the close button




############################# PARAMETERS PROPERTIES ##############################



#MAXIMUM_NEGATIVE_VALUE				=	-5000.0
MINIMUM_POSITIVE_VALUE				=	0.0
ONE_POSITIVE_VALUE					=	1.0
FIVE_POSITIVE_VALUE					=	5.0
MAXIMUM_POSITIVE_VALUE				=	5000.0


# Validators
# Double
VALID_D 							= 	QDoubleValidator()
VALID_POS_D 						= 	QDoubleValidator(MINIMUM_POSITIVE_VALUE, MAXIMUM_POSITIVE_VALUE, 1000)
VALID_POS_0_1_D 					= 	QDoubleValidator(MINIMUM_POSITIVE_VALUE, ONE_POSITIVE_VALUE, 1000)

# Integers
VALID_POS_I							= 	QIntValidator(FIVE_POSITIVE_VALUE, MAXIMUM_POSITIVE_VALUE)

# Any
VALID_ALL							=	"NOT A VALIDATOR"


MINIMUM_PARAMETER_AREA_WIDTH		=	200

PARAMETER_STYLESHEET				=	"font-size: 14px; font-family: Arial; font-weight: 600; margin-top: 15px; color: black;"
																			# Stylesheet for each parameter
TITLE_STYLESHEET					=	"font-size: 18px; font-family: Arial; font-weight: 600; margin-top: 25px; margin-bottom: 10px; color: black;"
																			# Stylesheet for title in parameter list
DIALOG_TEXT_STYLESHEET				=	"font-size: 14px; font-family: Arial; font-weight: 600; margin-top: 15px; color: black;"
																			# Stylesheet for text in dialog



################################ LAYOUT PROPERTIES ###############################



CONFIG_TAB_SPACING					=	20									# Spacing between widgets inside configTab

PARAMETERS_LAYOUT_PROPORTION		=	11									# How much should the parameters layout consume the window
SAVE_BUTTON_PROPORTION				=	1									# How much should the save button consume the window

GRAPH_LAYOUT_PROPORTION				=	3									# How much should the graph consume the window
CONFIG_LAYOUT_PROPORTION			=	1									# How much should the config layout consume the window



################################## PLOT SETTINGS #################################



MINIMUM_QUANTITY_POINTS				= 	5									# Minimum number of points to plot
MAXIMUM_QUANTITY_POINTS				= 	5000								# Maximum number of points to plot

CSV_GRAPH_TITLE						=	"I x Temperature"					# Title of gm graph
CSV_X_AXIS_TITLE					=	"Temperature (°C)"					# Title of X Axis for csv graph
CSV_Y_AXIS_TITLE					=	"I (A)"								# Title of Y Axis for csv graph

CURVE_CORRECTION_GRAPH_TITLE		=	"Igm x Ibeta"						# Title of curve correction graph
CURVE_CORRECTION_X_AXIS_TITLE		=	"Ibeta (A)"							# Title of X Axis for curve correction graph
CURVE_CORRECTION_Y_AXIS_TITLE		=	"Igm (A)"							# Title of Y Axis for curve correction graph

CURRENT_CURVE_GRAPH_TITLE			=	"gm x vd"							# Title of current curve graph
CURRENT_CURVE_X_AXIS_TITLE			=	"vd (V)"							# Title of X Axis for current curve graph
CURRENT_CURVE_Y_AXIS_TITLE			=	"gm (Siemens)"						# Title of Y Axis for current curve graph



################################# CONFIG SETTINGS ################################



CONFIG_SAVE_NAME					= 	"config_3_pares.json"				# Name of the save file (JSON)


# Hidden Configs
CONFIG_IGM_X_TEMP_PATH_KEY			=	"IGM_X_TEMP_PATH"					# The key for igmXtempPath value in JSON
CONFIG_IBETA_X_TEMP_PATH_KEY		=	"IBETA_X_TEMP_PATH"					# The key for ibetaXtempPath value in JSON


CONFIG_KEYS_HIDDEN					=	[CONFIG_IGM_X_TEMP_PATH_KEY, CONFIG_IBETA_X_TEMP_PATH_KEY]


DEFAULT_IGM_X_TEMP_PATH_VALUE 		= 	""									# The default value for igmXtempPath
DEFAULT_IBETA_X_TEMP_PATH_VALUE 	= 	""									# The default value for ibetaXtempPath


DEFAULT_VALUES_HIDDEN				=	[DEFAULT_IGM_X_TEMP_PATH_VALUE, DEFAULT_IBETA_X_TEMP_PATH_VALUE]


# Current Curve
CONFIG_K_KEY 						= 	"K"									# The key for k value in JSON
CONFIG_ICO_KEY						= 	"ICO"								# The key for ico value in JSON
CONFIG_TEMP_ICO_KEY					= 	"TEMP_ICO"							# The key for tempICo value in JSON
CONFIG_PHI_TO_KEY					= 	"PHI_TO"							# The key for phiTo value in JSON
CONFIG_KPO_KEY						=	"KPO"								# The key for kpo value in JSON
CONFIG_W_CENTRAL_KEY				=	"W_CENTRAL"							# The key for wCentral value in JSON
CONFIG_W_LATERAL_KEY				=	"W_LATERAL"							# The key for wLateral value in JSON
CONFIG_L_KEY						=	"L"									# The key for l value in JSON
CONFIG_ALPHA_KEY					=	"ALPHA"								# The key for alpha value in JSON
CONFIG_N_KEY						=	"N"									# The key for n value in JSON
CONFIG_ALPHA_U_KEY					=	"ALPHA_U"							# The key for alphaU value in JSON
CONFIG_ETA_KEY						=	"ETA"								# The key for eta value in JSON

CONFIG_STEP_VD_KEY					=	"STEP_VD"							# The key for stepVd value in JSON
CONFIG_VD_MAX_KEY					=	"VD_MAX"							# The key for vdMax value in JSON

CONFIG_INITIAL_IB_CENTRAL_KEY		=	"INITIAL_IB_CENTRAL"				# The key for initialIBCentral value in JSON
CONFIG_INITIAL_IB_LATERAL_KEY		=	"INITIAL_IB_LATERAL"				# The key for initialIBLateral value in JSON
CONFIG_IB_STEP_KEY					=	"IB_STEP"							# The key for ibStep value in JSON

CONFIG_INITIAL_TEMPERATURE_KEY		=	"INITIAL_TEMPERATURE"				# The key for initialTemp value in JSON
CONFIG_FINAL_TEMPERATURE_KEY		=	"FINAL_TEMPERATURE"					# The key for finalTemp value in JSON
CONFIG_STEP_TEMPERATURE_KEY			=	"STEP_TEMPERATURE"					# The key for stepTemp value in JSON

CONFIG_TARGET_GM_KEY				=	"TARGET_GM"							# The key for targetGM value in JSON
CONFIG_MAX_GM_DEVIATION_KEY			=	"MAX_GM_DEVIATION"					# The key for maxGMDeviation value in JSON

CONFIG_MAX_ITERATIONS_KEY			=	"MAX_ITERATIONS"					# The key for maxIterations value in JSON

CONFIG_INITIAL_VD_GRAPH_KEY			= 	"INITIAL_VD_GRAPH"					# The key for initialVdGraph value in JSON
CONFIG_FINAL_VD_GRAPH_KEY			= 	"FINAL_VD_GRAPH"					# The key for finalVdGraph value in JSON
CONFIG_POINTS_VD_GRAPH_KEY			= 	"POINTS_VD_GRAPH"					# The key for pointsVdGraph value in JSON


CONFIG_KEYS_CURRENT_CURVE			=	[]
'''										CONFIG_K_KEY, CONFIG_ICO_KEY, CONFIG_TEMP_ICO_KEY, CONFIG_PHI_TO_KEY,
										CONFIG_KPO_KEY, CONFIG_W_CENTRAL_KEY, CONFIG_W_LATERAL_KEY, CONFIG_L_KEY,
										CONFIG_ALPHA_KEY, CONFIG_N_KEY, CONFIG_ALPHA_U_KEY, CONFIG_ETA_KEY,
										CONFIG_STEP_VD_KEY, CONFIG_VD_MAX_KEY, CONFIG_INITIAL_IB_CENTRAL_KEY,
										CONFIG_INITIAL_IB_LATERAL_KEY, CONFIG_IB_STEP_KEY, CONFIG_INITIAL_TEMPERATURE_KEY,
										CONFIG_FINAL_TEMPERATURE_KEY, CONFIG_STEP_TEMPERATURE_KEY, CONFIG_TARGET_GM_KEY,
										CONFIG_MAX_GM_DEVIATION_KEY, CONFIG_MAX_ITERATIONS_KEY, CONFIG_INITIAL_VD_GRAPH_KEY,
										CONFIG_FINAL_VD_GRAPH_KEY, CONFIG_POINTS_VD_GRAPH_KEY
										]'''


# Simulated Annealing
CONFIG_IGM_COLUMN_NAME_KEY			= 	"IGM_COLUMN_NAME"					# The key for igmColumnName value in JSON
CONFIG_IBETA_COLUMN_NAME_KEY		= 	"IBETA_COLUMN_NAME"					# The key for ibetaColumnName value in JSON
CONFIG_TEMP_COLUMN_NAME_KEY			= 	"TEMP_COLUMN_NAME"					# The key for tempColumnName value in JSON

CONFIG_NUMBER_RECTS_KEY				= 	"NUMBER_RECTS"						# The key for numRects value in JSON
CONFIG_MAX_MB_KEY					=	"MAX_MB"							# The key for maxMB value in JSON
CONFIG_MAX_MC_KEY					=	"MAX_MC"							# The key for maxMC value in JSON
CONFIG_MAX_MD_KEY					=	"MAX_MD"							# The key for maxMD value in JSON
CONFIG_KB_KEY						= 	"KB"								# The key for kb value in JSON
CONFIG_INITIAL_TEMP_SA_KEY			= 	"INITIAL_TEMP_SA"					# The key for initialTempSA value in JSON
CONFIG_FINAL_TEMP_SA_KEY			= 	"FINAL_TEMP_SA"						# The key for finalTempSA value in JSON
CONFIG_COOLING_RATE_KEY				= 	"COOLING_RATE"						# The key for coolingRate value in JSON
CONFIG_MAX_ITERATIONS_SA_KEY		= 	"MAX_ITERATIONS_SA"					# The key for iterationsMaxSA value in JSON

CONFIG_CSV_SEPARATOR_KEY			= 	"CSV_SEPARATOR"						# The key for csvSeparator value in JSON


CONFIG_KEYS_SA						=	[
										CONFIG_IGM_COLUMN_NAME_KEY, CONFIG_IBETA_COLUMN_NAME_KEY, CONFIG_TEMP_COLUMN_NAME_KEY,
										CONFIG_NUMBER_RECTS_KEY, CONFIG_MAX_MB_KEY, CONFIG_MAX_MC_KEY, CONFIG_MAX_MD_KEY,
										CONFIG_KB_KEY, CONFIG_INITIAL_TEMP_SA_KEY, CONFIG_FINAL_TEMP_SA_KEY,
										CONFIG_COOLING_RATE_KEY, CONFIG_MAX_ITERATIONS_SA_KEY, CONFIG_CSV_SEPARATOR_KEY
										]


# Current Curve
DEFAULT_K_VALUE 					= 	0.1									# The default value for k
DEFAULT_ICO_VALUE					= 	3.0									# The default value for ico
DEFAULT_TEMP_ICO_VALUE				= 	27.0								# The default value for tempICo
DEFAULT_PHI_TO_VALUE				= 	0.71								# The default value for phiTo
DEFAULT_KPO_VALUE					= 	74.4e-6								# The default value for kpo
DEFAULT_W_CENTRAL_VALUE				= 	50e-6								# The default value for wCentral
DEFAULT_W_LATERAL_VALUE				= 	5e-6								# The default value for wLateral
DEFAULT_L_VALUE						= 	180e-6								# The default value for l
DEFAULT_ALPHA_VALUE					= 	1.21								# The default value for alpha
DEFAULT_N_VALUE						= 	1.6									# The default value for n
DEFAULT_ALPHA_U_VALUE				= 	-1.2								# The default value for alphaU
DEFAULT_ETA_VALUE					= 	0.043499							# The default value for eta

DEFAULT_STEP_VD_VALUE				=	0.05								# The default value for stepVd
DEFAULT_VD_MAX_VALUE				=	1.5									# The default value for vdMax

DEFAULT_INITIAL_IB_CENTRAL_VALUE	=	5.332e-05							# The default value for initialIBCentral
DEFAULT_INITIAL_IB_LATERAL_VALUE	=	5.332e-05							# The default value for initialIBLateral
DEFAULT_IB_STEP_VALUE				=	5e-07								# The default value for ibStep

DEFAULT_INITIAL_TEMPERATURE_VALUE	=	-50.0								# The default value for initialTemp
DEFAULT_FINAL_TEMPERATURE_VALUE		=	175.0								# The default value for finalTemp
DEFAULT_STEP_TEMPERATURE_VALUE		=	15.0								# The default value for stepTemp

DEFAULT_TARGET_GM_VALUE				=	100e-6								# The default value for targetGM
DEFAULT_MAX_GM_DEVIATION_VALUE		=	1e-5								# The default value for maxGMDeviation

DEFAULT_MAX_ITERATIONS_VALUE		=	50									# The default value for maxIterations

DEFAULT_INITIAL_VD_GRAPH_VALUE		= 	-2.3								# The default value for initialVdGraph
DEFAULT_FINAL_VD_GRAPH_VALUE		= 	2.3									# The default value for finalVdGraph
DEFAULT_POINTS_VD_GRAPH_VALUE		= 	300									# The default value for pointsVdGraph


DEFAULT_VALUES_CURRENT_CURVE		=	[
										DEFAULT_K_VALUE, DEFAULT_ICO_VALUE, DEFAULT_TEMP_ICO_VALUE, DEFAULT_PHI_TO_VALUE,
										DEFAULT_KPO_VALUE, DEFAULT_W_CENTRAL_VALUE, DEFAULT_W_LATERAL_VALUE, DEFAULT_L_VALUE,
										DEFAULT_ALPHA_VALUE, DEFAULT_N_VALUE, DEFAULT_ALPHA_U_VALUE, DEFAULT_ETA_VALUE,
										DEFAULT_STEP_VD_VALUE, DEFAULT_VD_MAX_VALUE, DEFAULT_INITIAL_IB_CENTRAL_VALUE,
										DEFAULT_INITIAL_IB_LATERAL_VALUE, DEFAULT_IB_STEP_VALUE, DEFAULT_INITIAL_TEMPERATURE_VALUE,
										DEFAULT_FINAL_TEMPERATURE_VALUE, DEFAULT_STEP_TEMPERATURE_VALUE, DEFAULT_TARGET_GM_VALUE,
										DEFAULT_MAX_GM_DEVIATION_VALUE, DEFAULT_MAX_ITERATIONS_VALUE, DEFAULT_INITIAL_VD_GRAPH_VALUE,
										DEFAULT_FINAL_VD_GRAPH_VALUE, DEFAULT_POINTS_VD_GRAPH_VALUE
										]


DEFAULT_CAPTIONS_CURRENT_CURVE		=	[
										"K", "ICo", "Temperature of ICo", "Phi T0", "Kp0", "W Central", "W Lateral", "L",
										"Alpha", "N", "Alpha U", "Eta", "Step Vd", "Maximum Vd", "Initial IB Central",
										"Initial IB Lateral", "IB Step", "Initial Temperature", "Final Temperature",
										"Step Temperature", "Target GM", "Maximum GM Deviation", "Maximum Iterations",
										"Initial Vd for Graph", "Final Vd for Graph", "Points for Graph"
										]


DEFAULT_VALIDATORS_CURRENT_CURVE	=	[
										VALID_POS_0_1_D, VALID_POS_D, VALID_D, VALID_POS_D, VALID_POS_D, VALID_POS_D, VALID_POS_D,
										VALID_POS_D, VALID_POS_D, VALID_POS_D, VALID_D, VALID_D, VALID_POS_D, VALID_POS_D, VALID_D,
										VALID_D, VALID_POS_D, VALID_D, VALID_D, VALID_POS_D, VALID_POS_D, VALID_POS_D, VALID_POS_I,
										VALID_D, VALID_D, VALID_POS_I
										]


# Simulated Annealing
DEFAULT_IGM_COLUMN_NAME_VALUE		= 	"Igm"								# The default name of the Igm column in the csv file
DEFAULT_IBETA_COLUMN_NAME_VALUE		= 	"Ibeta"								# The default name of the Ibeta (Iin) column in the csv file
DEFAULT_TEMP_COLUMN_NAME_VALUE		= 	"Temperature"						# The default name of the temperature column in the csv file

DEFAULT_NUMBER_RECTS_VALUE			= 	3									# The default value for numRects
DEFAULT_MAX_MB_VALUE				=	10									# The default value for maxMB
DEFAULT_MAX_MC_VALUE				=	20									# The default value for maxMC
DEFAULT_MAX_MD_VALUE				=	20									# The default value for maxMD
DEFAULT_KB_VALUE 					= 	0.1									# The default value for kb
DEFAULT_INITIAL_TEMP_SA_VALUE		= 	50									# The default value for initialTempSA
DEFAULT_FINAL_TEMP_SA_VALUE			= 	0.01								# The default value for finalTempSA
DEFAULT_COOLING_RATE_VALUE			= 	0.01								# The default value for coolingRate
DEFAULT_MAX_ITERATIONS_SA_VALUE		= 	100									# The default value for iterationsMaxSA

DEFAULT_CSV_SEPARATOR_VALUE			= 	";"									# The default value for csvSeparator


DEFAULT_VALUES_SA					=	[
										DEFAULT_IGM_COLUMN_NAME_VALUE, DEFAULT_IBETA_COLUMN_NAME_VALUE, DEFAULT_TEMP_COLUMN_NAME_VALUE,
										DEFAULT_NUMBER_RECTS_VALUE, DEFAULT_MAX_MB_VALUE, DEFAULT_MAX_MC_VALUE,
										DEFAULT_MAX_MD_VALUE, DEFAULT_KB_VALUE, DEFAULT_INITIAL_TEMP_SA_VALUE, 
										DEFAULT_FINAL_TEMP_SA_VALUE, DEFAULT_COOLING_RATE_VALUE, DEFAULT_MAX_ITERATIONS_SA_VALUE,
										DEFAULT_CSV_SEPARATOR_VALUE
										]


DEFAULT_CAPTIONS_SA					=	[
										"Igm CSV Column Name", "Ibeta CSV Column Name", "Temperature CSV Column Name",
										"Number of Rects", "Maximum MB", "Maximum MC", "Maximum MD", "KB", "Initial Temperature SA",
										"Final Temperature SA", "Cooling Rate", "Maximum Iterations SA", "CSV Separator"
										]


DEFAULT_VALIDATORS_SA				=	[
										VALID_ALL, VALID_ALL, VALID_ALL, VALID_POS_I, VALID_POS_I, VALID_POS_I, VALID_POS_I, 
										VALID_POS_D, VALID_D, VALID_D, VALID_POS_D, VALID_POS_I, VALID_ALL
										]



# List of Integers and Strings parameters
INTEGERS_LIST						=	[
										CONFIG_MAX_ITERATIONS_KEY, CONFIG_POINTS_VD_GRAPH_KEY, CONFIG_NUMBER_RECTS_KEY,
										CONFIG_MAX_MB_KEY, CONFIG_MAX_MC_KEY, CONFIG_MAX_MD_KEY, CONFIG_MAX_ITERATIONS_SA_KEY
										]


STRINGS_LIST						=	[
										CONFIG_IGM_COLUMN_NAME_KEY, CONFIG_IBETA_COLUMN_NAME_KEY, 
										CONFIG_TEMP_COLUMN_NAME_KEY, CONFIG_CSV_SEPARATOR_KEY
										]


############################### STATUS PROPERTIES ################################



OK_STATUS_TEXT						= 	"Ready."									# Status text when nothing is being done
SAVING_STATUS_TEXT					= 	"Saving..."									# Status text when something is being saved
LOADING_STATUS_TEXT					= 	"Loading..."								# Status text when something is being loaded
CALCULATING_STATUS_TEXT				= 	"Calculating..."							# Status text when something is being calculated
ERROR_IGM_X_TEMP_CSV_TEXT			=	"Error opening Igm x Temp file!"			# Status text when igm x temp is not valid
ERROR_IBETA_X_TEMP_CSV_TEXT			=	"Error opening Ibeta X Temp file!"			# Status text when ibeta x temp is not valid
ERROR_CENTRAL_IB_X_TEMP_CSV_TEXT	=	"Error saving central IB X Temp file!"		# Status text when igm x temp is not valid
ERROR_LATERAL_IB_X_TEMP_CSV_TEXT	=	"Error saving lateral IB X Temp file!"		# Status text when ibeta x temp is not valid
ERROR_READING_CSV_TEXT				=	"Error reading CSV files!"					# Status text when failed to read CSV files
ERROR_MERGING_CSV_TEXT				=	"Error merging CSV files! Make sure columns names matches"					
																					# Status text when failed to merge CSV files due to a column name mismatch
ERROR_READING_CSV_COLUMN_TEXT		=	"Error reading CSV columns!"				# Status text when failed to read CSV columns properly


OK_STATUS_STYLESHEET				=	"font-size: 18px; font-family: Arial; font-weight: 600; margin-top: 15px; color: green;"
																			# Stylesheet for Ok status
PROCESSING_STATUS_STYLESHEET		=	"font-size: 18px; font-family: Arial; font-weight: 600; margin-top: 15px; color: blue;"
																			# Stylesheet for Ok status
FAILED_STATUS_STYLESHEET			=	"font-size: 18px; font-family: Arial; font-weight: 600; margin-top: 15px; color: red;"
																			# Stylesheet for Failed status



################################# CSV PROPERTIES #################################



#IGM_COLUMN_NAME 					= 	"Igm"							# The name of the Igm column in the csv file
#IBETA_COLUMN_NAME 					= 	"Ibeta"							# The name of the Ibeta (Iin) column in the csv file
#TEMPERATURE_COLUMN_NAME 			= 	"Temperature"					# The name of the temperature column in the csv file

CENTRAL_IB_COLUMN_NAME 				= 	"CentralIB"						# The name of the centralIB column in the csv file
LATERAL_IB_COLUMN_NAME 				= 	"LateralIB"						# The name of the lateralIB column in the csv file


IGM_X_TEMP_CSV_OPEN_CAPTION			=	"Open Igm x Temp csv"			# Caption of the file dialog to open Igm x Temp
IBETA_X_TEMP_CSV_OPEN_CAPTION		=	"Open Ibeta x Temp csv"			# Caption of the file dialog to open Ibeta x Temp


IGM_X_TEMP_FILEPATH 				= 	"csv/Igm_X_T-IC-0.01.csv"		# The filepath to Igm x Temp
IBETA_X_TEMP_FILEPATH 				= 	"csv/Ibeta_X_T.csv"				# The filepath to Ibeta x Temp (Iin x Temp)
#CSV_SEPARATOR						=	";"								# The separator for the csv



################################# OTHER CONFIG #################################



USE_CREATE_CURRENT_CURVE			=	False							# Should it create widgets to current curve algorithm