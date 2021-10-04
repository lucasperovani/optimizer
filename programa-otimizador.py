import config_3_pares as config
import sys

from threading import Thread

import numpy as np
import pandas as pd

from pathlib import Path
import json

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QDialog
from PySide2.QtWidgets import QHBoxLayout, QSpacerItem, QSplitter, QPushButton
from PySide2.QtWidgets import QSizePolicy, QScrollArea, QLineEdit, QLabel, QFileDialog
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize, Slot, Signal, Qt, SIGNAL, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import ekv_solver_lib as ekv
import current_correction as curCorrection
#import current_curve as curCurve


'''
class currentCurveThread(Thread):
	
	
	def __init__(self, graph, statusEdit, variables, saveFunction):

		Thread.__init__(self)


		# Set variables
		self.graph 				= graph

		self.statusEdit 		= statusEdit

		self.k 							= variables[config.CONFIG_K_KEY]
		self.ico 						= variables[config.CONFIG_ICO_KEY]
		self.tempICo 					= variables[config.CONFIG_TEMP_ICO_KEY]
		self.phiTo 						= variables[config.CONFIG_PHI_TO_KEY]
		self.kpo 						= variables[config.CONFIG_KPO_KEY]
		self.wCentral 					= variables[config.CONFIG_W_CENTRAL_KEY]
		self.wLateral 					= variables[config.CONFIG_W_LATERAL_KEY]
		self.l 							= variables[config.CONFIG_L_KEY]
		self.alpha 						= variables[config.CONFIG_ALPHA_KEY]
		self.n 							= variables[config.CONFIG_N_KEY]
		self.alphaU 					= variables[config.CONFIG_ALPHA_U_KEY]
		self.eta 						= variables[config.CONFIG_ETA_KEY]

		self.stepVd 					= variables[config.CONFIG_STEP_VD_KEY]
		self.vdMax 						= variables[config.CONFIG_VD_MAX_KEY]

		self.initialIBCentral 			= variables[config.CONFIG_INITIAL_IB_CENTRAL_KEY]
		self.initialIBLateral 			= variables[config.CONFIG_INITIAL_IB_LATERAL_KEY]
		self.ibStep 					= variables[config.CONFIG_IB_STEP_KEY]

		self.initialTemp 				= variables[config.CONFIG_INITIAL_TEMPERATURE_KEY]
		self.finalTemp 					= variables[config.CONFIG_FINAL_TEMPERATURE_KEY]
		self.stepTemp 					= variables[config.CONFIG_STEP_TEMPERATURE_KEY]

		self.targetGM 					= variables[config.CONFIG_TARGET_GM_KEY]
		self.maxGMDeviation 			= variables[config.CONFIG_MAX_GM_DEVIATION_KEY]

		self.maxIterations 				= variables[config.CONFIG_MAX_ITERATIONS_KEY]

		self.initialVdGraph 			= variables[config.CONFIG_INITIAL_VD_GRAPH_KEY]
		self.finalVdGraph 				= variables[config.CONFIG_FINAL_VD_GRAPH_KEY]
		self.pointsVdGraph 				= variables[config.CONFIG_POINTS_VD_GRAPH_KEY]

		self.saveData					= saveFunction


		# Create the Object
		self.curCurve = curCurve.curveIB(	self.k, self.ico, self.tempICo, self.phiTo, self.kpo, self.alpha, 
											self.wCentral, self.wLateral, self.l, self.n, self.alphaU, self.eta	)



	def run(self):

		centralIBVector, lateralIBVector = self.curCurve.getIBCurve(self.initialIBCentral, self.initialIBLateral,
																	self.ibStep, self.initialTemp, self.finalTemp,
																	self.stepTemp, self.targetGM, self.maxGMDeviation,
																	self.maxIterations, self.stepVd, self.vdMax)


		# Interval
		vd = np.linspace(self.initialVdGraph, self.finalVdGraph, self.pointsVdGraph)


		# Variables
		legends = []

		data 	= np.zeros(( len(centralIBVector), 2, self.pointsVdGraph ))

		graph	= 0
		point	= 0


		# Loop every pair temperature and IB
		for centralTempAndIB, lateralTempAndIB in zip(centralIBVector, lateralIBVector):


			# Loop every vd point
			for vdPoint in vd:

				# Calculate gm
				gmPoint = self.curCurve.getGm(vdPoint, centralTempAndIB[1], lateralTempAndIB[1], centralTempAndIB[0])


				# Add to data
				data[graph][0][point] = vdPoint
				data[graph][1][point] = gmPoint

				point += 1


			# Add legend
			legends.append('Temperatura: ' + str(centralTempAndIB[0]) + '°C')

			graph += 1
			point = 0


		# Prepare data
		xinferior = self.initialVdGraph
		xsuperior = self.finalVdGraph
		yinferior = 0.0
		ysuperior = self.targetGM * 1.1

		
		self.graph.updatePlot(data, xinferior, xsuperior, yinferior, ysuperior, config.CURRENT_CURVE_GRAPH_TITLE, 
							  config.CURRENT_CURVE_X_AXIS_TITLE, config.CURRENT_CURVE_Y_AXIS_TITLE, legends)


		# Set status text to OK
		self.statusEdit.setText(config.OK_STATUS_TEXT)
		self.statusEdit.setStyleSheet(config.OK_STATUS_STYLESHEET)


		# Save data
		self.saveData({"central": centralIBVector, "lateral": lateralIBVector})
'''


class currentCorrectionThread(Thread):

	def __init__(self, graph, statusEdit, variables, saveData, igmXtempCsv=config.IGM_X_TEMP_FILEPATH, ibetaXtempCsv=config.IBETA_X_TEMP_FILEPATH):

		Thread.__init__(self)


		# Set variables
		self.graph 				= graph

		self.statusEdit 		= statusEdit

		self.igmColumnName 		= variables[config.CONFIG_IGM_COLUMN_NAME_KEY]
		self.ibetaColumnName 	= variables[config.CONFIG_IBETA_COLUMN_NAME_KEY]
		self.tempColumnName 	= variables[config.CONFIG_TEMP_COLUMN_NAME_KEY]
	
		self.numRects 			= variables[config.CONFIG_NUMBER_RECTS_KEY]
		self.maxMB 				= variables[config.CONFIG_MAX_MB_KEY]
		self.maxMC 				= variables[config.CONFIG_MAX_MC_KEY]
		self.maxMD 				= variables[config.CONFIG_MAX_MD_KEY]

		self.kb 				= variables[config.CONFIG_KB_KEY]
		self.initialTempSA 		= variables[config.CONFIG_INITIAL_TEMP_SA_KEY]
		self.finalTempSA 		= variables[config.CONFIG_FINAL_TEMP_SA_KEY]
		self.coolingRate 		= variables[config.CONFIG_COOLING_RATE_KEY]
		self.iterationsMaxSA 	= variables[config.CONFIG_MAX_ITERATIONS_SA_KEY]

		self.csvSeparator		= variables[config.CONFIG_CSV_SEPARATOR_KEY]
		self.saveData			= saveData

		self.igmXtempCsv		= igmXtempCsv
		self.ibetaXtempCsv		= ibetaXtempCsv



	def run(self):

		legends = ["Original IB", "Simulated Annealing IB"]


		# Read the input graphs
		try:
			igm_x_temp 			= pd.read_csv(self.igmXtempCsv, sep = self.csvSeparator)
			ibeta_x_temp 		= pd.read_csv(self.ibetaXtempCsv, sep = self.csvSeparator)

		except:
			self.statusEdit.setText(config.ERROR_READING_CSV_TEXT)
			self.statusEdit.setStyleSheet(config.FAILED_STATUS_STYLESHEET)
			return


		# Merge both datasets together
		try:
			igm_x_ibeta 		= pd.merge(igm_x_temp, ibeta_x_temp, on = self.tempColumnName)
		
		except:
			self.statusEdit.setText(config.ERROR_MERGING_CSV_TEXT)
			self.statusEdit.setStyleSheet(config.FAILED_STATUS_STYLESHEET)
			return


		# Remove temperature column
		igm_x_ibeta 		= igm_x_ibeta.drop(columns = self.tempColumnName)


		# Make dataframe as an array to numpy
		igm_x_ibeta_numpy 	= igm_x_ibeta.to_numpy()


		# Create a new random piecewise current
		initial_config = curCorrection.current_piecewise(self.numRects, igm_x_ibeta_numpy, max_Mb=self.maxMB, 
														 max_Mc=self.maxMC, max_Md=self.maxMD)


		# Run the Simulated Annealing over the created current piecewise
		simu_anneal = curCorrection.simulated_annealing(initial_config, self.initialTempSA, self.finalTempSA, 
														self.iterationsMaxSA, self.kb, self.coolingRate)
		best = simu_anneal.run(self.saveData)


		# Print the info about the best
		print("\n#################################### BEST ###################################\n")
		best.print_piecewise()
		print("\nNRMSE: " + str(best.energy_cost()))
		print("\n#################################### END ####################################\n")


		# Send the data to be saved and shown
		self.saveData(best)


		# Prepare data
		data = np.zeros((2, 2, len(igm_x_ibeta_numpy)))
		point = 0

		xinferior = igm_x_ibeta_numpy[0][1]
		xsuperior = igm_x_ibeta_numpy[0][1]
		yinferior = igm_x_ibeta_numpy[0][0]
		ysuperior = igm_x_ibeta_numpy[0][0]

		for current_point in igm_x_ibeta_numpy:

			# Append data
			data[0][0][point] = current_point[1]
			data[0][1][point] = current_point[0]

			data[1][0][point] = current_point[1]


			# Calculate limits
			if current_point[1] < xinferior:
				xinferior = current_point[1]
			
			if current_point[1] > xsuperior:
				xsuperior = current_point[1]
			
			if current_point[0] < yinferior:
				yinferior = current_point[0]
			
			if current_point[0] > ysuperior:
				ysuperior = current_point[0]

			
			point += 1
		
		data[1][1] = best.plot(data[1][0])

		
		self.graph.updatePlot(data, xinferior, xsuperior, yinferior, ysuperior, config.CURVE_CORRECTION_GRAPH_TITLE, 
							  config.CURVE_CORRECTION_X_AXIS_TITLE, config.CURVE_CORRECTION_Y_AXIS_TITLE, legends)


		# Set status text to OK
		self.statusEdit.setText(config.OK_STATUS_TEXT)
		self.statusEdit.setStyleSheet(config.OK_STATUS_STYLESHEET)

		return



class plotCsvsThread(Thread):

	def __init__(self, graph, statusEdit, csvSeparator=config.DEFAULT_CSV_SEPARATOR_VALUE, igmXtempCsv = "", ibetaXtempCsv = "",
				igmColumnName=config.DEFAULT_IGM_COLUMN_NAME_VALUE, ibetaColumnName=config.DEFAULT_IBETA_COLUMN_NAME_VALUE,
				tempColumnName=config.DEFAULT_TEMP_COLUMN_NAME_VALUE):


		Thread.__init__(self)

		self.csvSeparator			= csvSeparator

		self.igmColumnName			= igmColumnName
		self.ibetaColumnName		= ibetaColumnName
		self.tempColumnName			= tempColumnName

		self.igmXtempCsv			= igmXtempCsv
		self.ibetaXtempCsv			= ibetaXtempCsv

		self.statusEdit				= statusEdit

		self.graph					= graph



	def run(self):

		# Check if csvs are valid
		if self.igmXtempCsv == "":
			# Set status text to ERROR
			self.statusEdit.setText(config.ERROR_IGM_X_TEMP_CSV_TEXT)
			self.statusEdit.setStyleSheet(config.FAILED_STATUS_STYLESHEET)

			return
		

		if self.ibetaXtempCsv == "":
			# Set status text to ERROR
			self.statusEdit.setText(config.ERROR_IBETA_X_TEMP_CSV_TEXT)
			self.statusEdit.setStyleSheet(config.FAILED_STATUS_STYLESHEET)

			return


		# Plot
		legends = ["Igm", "Ibeta"]


		# Read csvs
		igm_x_temp 			= pd.read_csv(self.igmXtempCsv, sep = self.csvSeparator)
		ibeta_x_temp 		= pd.read_csv(self.ibetaXtempCsv, sep = self.csvSeparator)


		data = np.zeros((2, 2, max(len(igm_x_temp), len(ibeta_x_temp))))


		try:
			for count in range(0, len(igm_x_temp)):
				data[0][0][count] 		= igm_x_temp[self.tempColumnName].to_numpy()[count]
				data[0][1][count] 		= igm_x_temp[self.igmColumnName].to_numpy()[count]

		except:
			self.statusEdit.setText(config.ERROR_READING_CSV_COLUMN_TEXT)
			self.statusEdit.setStyleSheet(config.FAILED_STATUS_STYLESHEET)
			return

		try:
			for count in range(0, len(ibeta_x_temp)):
				data[1][0][count] 		= ibeta_x_temp[self.tempColumnName].to_numpy()[count]
				data[1][1][count] 		= ibeta_x_temp[self.ibetaColumnName].to_numpy()[count]
			
		except:
			self.statusEdit.setText(config.ERROR_READING_CSV_COLUMN_TEXT)
			self.statusEdit.setStyleSheet(config.FAILED_STATUS_STYLESHEET)
			return
		

		xMin = min(igm_x_temp[self.tempColumnName].min(), ibeta_x_temp[self.tempColumnName].min())
		xMax = max(igm_x_temp[self.tempColumnName].max(), ibeta_x_temp[self.tempColumnName].max())

		yMin = min(igm_x_temp[self.igmColumnName].min(), ibeta_x_temp[self.ibetaColumnName].min())
		yMax = max(igm_x_temp[self.igmColumnName].max(), ibeta_x_temp[self.ibetaColumnName].max())


		# Try fixing missing values
		data[0][0] = np.where(data[0][0] != 0, data[0][0], xMax)
		data[0][1] = np.where(data[0][1] != 0, data[0][1], yMax)
		data[1][0] = np.where(data[1][0] != 0, data[1][0], xMax)
		data[1][1] = np.where(data[1][1] != 0, data[1][1], yMax)


		# Plot curve
		self.graph.updatePlot(data, xMin, xMax, 0.9*yMin, yMax*1.1, 
			config.CSV_GRAPH_TITLE, config.CSV_X_AXIS_TITLE, config.CSV_Y_AXIS_TITLE,legends)


		# Set status text to OK
		self.statusEdit.setText(config.OK_STATUS_TEXT)
		self.statusEdit.setStyleSheet(config.OK_STATUS_STYLESHEET)



class MatplotlibWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		figure = Figure(figsize=(7, 5), dpi=65, facecolor=(0.5, 0.5, 0.5), edgecolor=(0, 0, 0))
		self.canvas = FigureCanvas(figure)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.toolbar.setStyleSheet(config.MATPLOTLIB_TOOLBAR_STYLESHEET)
		layout = QVBoxLayout(self)
		layout.setSpacing(0)
		layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)

		self.ax = figure.add_subplot(111)
		self.line, *_ = self.ax.plot([])

	@Slot(list)
	def updatePlot(self, data, xInferior, xSuperior, yInferior, ySuperior, title="", xAxisTitle="", yAxisTitle="", legends=[]):
		#self.line.set_data(range(len(data)), data)
		#self.line.set_data(data[0])

		self.ax.cla()

		self.ax.set_xlim(xInferior, xSuperior)
		self.ax.set_ylim(yInferior, ySuperior)


		for curve in data:
			self.ax.plot(curve[0], curve[1])


		self.ax.legend(legends)
		self.ax.set_title (title)
		self.ax.set_xlabel (xAxisTitle)
		self.ax.set_ylabel (yAxisTitle)

		self.canvas.draw()



class mainWindow(QMainWindow):

	def __init__(self, parent=None):
		super(mainWindow, self).__init__(parent)


		# Start variables
		self.igmXtempCsv = ""
		self.ibetaXtempCsv = ""
		self.edits = {}
		self.data = {}
		self.hidden = {}
		self.settedData = False


		# Create the timer
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updateStatus)


		# Create the layout
		self.createLayout()


		# Load savefile
		self.load()


		# Connections
		self.igmXtempButton.clicked.connect(lambda: self.openigmXtemp())
		self.ibetaXtempButton.clicked.connect(lambda: self.openibetaXtemp())

		self.configButton.clicked.connect(lambda: self.toggleTabMenu())
		self.saveButton.clicked.connect(lambda: self.save())

		self.plotCsvsButton.clicked.connect(lambda: self.plotCsvs())
		if config.USE_CREATE_CURRENT_CURVE:
			self.curveCurrentButton.clicked.connect(lambda: self.generateCurrentCurve())
		self.curveCorretionButton.clicked.connect(lambda: self.generateCurrentCorrection())



	def createLayout(self):

		# Set basic parameters of application
		self.setWindowTitle(config.TITLE)
		self.setWindowIcon(QIcon(config.ICON_PATH))
		self.setMinimumSize(config.WIDTH, config.HEIGHT)


		self.mainWidget = QWidget()
		self.mainWidget.setStyleSheet(config.BACKGROUND_STYLESHEET)
		self.setCentralWidget(self.mainWidget)


		# Add a new layout
		self.appLayout = QHBoxLayout()
		self.appLayout.setContentsMargins(config.LEFT_MARGIN, config.TOP_MARGIN, config.RIGHT_MARGIN, config.BOTTOM_MARGIN)
		self.mainWidget.setLayout(self.appLayout)


		# Add the layout to store graph related stuff
		self.graphLayout = QVBoxLayout()
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.appLayout.addLayout(self.graphLayout)


		# Add the graph
		self.graph = MatplotlibWidget()
		self.graphLayout.addWidget(self.graph)


		# Add status text
		self.statusText = QLabel(config.OK_STATUS_TEXT)
		self.statusText.setStyleSheet(config.OK_STATUS_STYLESHEET)
		self.graphLayout.addWidget(self.statusText)


		# Add buttons to calculate current curve and current correction
		buttonsLayout 					= QHBoxLayout()

		self.plotCsvsButton 			= QPushButton(config.CSVS_PLOT_BUTTON_TEXT)
		buttonsLayout.addWidget(self.plotCsvsButton)

		if config.USE_CREATE_CURRENT_CURVE:
			self.curveCurrentButton 		= QPushButton(config.CURVE_CURRENT_BUTTON_TEXT)
			self.curveCurrentButton.setStyleSheet(config.CURVE_CURRENT_BUTTON_STYLESHEET)
			self.curveCurrentButton.setFixedHeight(config.CURVE_CURRENT_BUTTON_HEIGHT)
			buttonsLayout.addWidget(self.curveCurrentButton)

		self.curveCorretionButton 		= QPushButton(config.CURVE_CORRECTION_BUTTON_TEXT)
		buttonsLayout.addWidget(self.curveCorretionButton)

		self.plotCsvsButton.setStyleSheet(config.CSVS_PLOT_BUTTON_STYLESHEET)
		self.curveCorretionButton.setStyleSheet(config.CURVE_CORRECTION_BUTTON_STYLESHEET)

		self.plotCsvsButton.setFixedHeight(config.CSVS_PLOT_BUTTON_HEIGHT)
		self.curveCorretionButton.setFixedHeight(config.CURVE_CORRECTION_BUTTON_HEIGHT)

		self.graphLayout.addLayout(buttonsLayout)


		# Adjust proportions of graphLayout
		self.graphLayout.setStretch(0, 1)


		# Add a config tab button
		self.tabOpened = False		# Controls the toggle of the tab menu

		self.configButton = QPushButton(QIcon(config.CONFIG_BUTTON_ICON), "")
		self.configButton.setStyleSheet(config.CONFIG_BUTTON_STYLESHEET)
		#self.configButton.setFlat(True)
		self.configButton.setIconSize(QSize(config.CONFIG_BUTTON_SIZE, config.CONFIG_BUTTON_SIZE))
		self.configButton.setFixedSize(config.CONFIG_BUTTON_SIZE, config.CONFIG_BUTTON_SIZE)

		self.appLayout.addWidget(self.configButton)
		self.appLayout.setAlignment(self.configButton, Qt.AlignTop)


		# Add the config tab
		self.configTab = QWidget()
		self.appLayout.addWidget(self.configTab)
		self.configTab.hide()

		self.configLayout = QVBoxLayout()
		self.configTab.setLayout(self.configLayout)


		# Setup config tab
		self.setupConfigTab()



	def toggleTabMenu(self):

		# Change the state of the tab menu
		self.tabOpened = not self.tabOpened


		# Change visibility
		if self.tabOpened:
			self.configTab.show()
		else:
			self.configTab.hide()



	def setupConfigTab(self):

		# Add a scrollable area for parameters
		self.parametersScrollArea = QScrollArea()
		self.parametersScrollArea.setMinimumWidth(config.MINIMUM_PARAMETER_AREA_WIDTH)
		self.parametersScrollArea.setWidgetResizable(True)
		self.configLayout.addWidget(self.parametersScrollArea)
		self.configLayout.setSpacing(config.CONFIG_TAB_SPACING)

		self.parametersScrollWidget = QWidget()
		self.parametersScrollArea.setWidget(self.parametersScrollWidget)
		

		# Add a save button
		self.saveButton = QPushButton(config.SAVE_BUTTON_TEXT)
		self.saveButton.setStyleSheet(config.SAVE_BUTTON_STYLESHEET)
		self.saveButton.setFixedHeight(config.SAVE_BUTTON_SIZE)

		self.configLayout.addWidget(self.saveButton)


		# Set the size of the layout
		self.configLayout.setStretch(0, config.PARAMETERS_LAYOUT_PROPORTION)
		self.configLayout.setStretch(1, config.SAVE_BUTTON_PROPORTION) 

		self.appLayout.setStretch(0, config.GRAPH_LAYOUT_PROPORTION)
		self.appLayout.setStretch(2, config.CONFIG_LAYOUT_PROPORTION)


		# Create parameters
		self.createParameters()



	def createParameters(self):


		# Set parameters layout
		self.parametersLayout = QVBoxLayout()
		self.parametersLayout.setAlignment(Qt.AlignTop)
		self.parametersScrollWidget.setLayout(self.parametersLayout)


		# Add parameters
		# Current Curve Section
		if config.USE_CREATE_CURRENT_CURVE:
			ccTitle = QLabel("-- Current Curve Settings --")
			ccTitle.setStyleSheet(config.TITLE_STYLESHEET)
			ccTitle.setAlignment(Qt.AlignCenter)
			self.parametersLayout.addWidget(ccTitle)

		
		configKeys 	= config.CONFIG_KEYS_CURRENT_CURVE
		captions	= config.DEFAULT_CAPTIONS_CURRENT_CURVE
		validators	= config.DEFAULT_VALIDATORS_CURRENT_CURVE


		for configKey, caption, validator in zip(configKeys, captions, validators):
			self.createEdit(configKey, caption, validator)
		

		# Simulated Annealing Section
		saTitle = QLabel("-- SA Settings --")
		saTitle.setStyleSheet(config.TITLE_STYLESHEET)
		saTitle.setAlignment(Qt.AlignCenter)
		self.parametersLayout.addWidget(saTitle)


		#	IGM_X_TEMP_FILE
		igmXtempText = QLabel("Igm x Temperature csv:")
		igmXtempText.setStyleSheet(config.PARAMETER_STYLESHEET)
		self.igmXtempButton = QPushButton(config.CSV_BUTTON_TEXT)
		self.igmXtempButton.setFixedHeight(config.CSV_BUTTON_HEIGHT)
		self.igmXtempButton.setStyleSheet(config.CSV_BUTTON_STYLESHEET)
		self.parametersLayout.addWidget(igmXtempText)
		self.parametersLayout.addWidget(self.igmXtempButton)


		#	IBETA_X_TEMP_FILE
		ibetaXtempText = QLabel("Ibeta x Temperature csv:")
		ibetaXtempText.setStyleSheet(config.PARAMETER_STYLESHEET)
		self.ibetaXtempButton = QPushButton(config.CSV_BUTTON_TEXT)
		self.ibetaXtempButton.setFixedHeight(config.CSV_BUTTON_HEIGHT)
		self.ibetaXtempButton.setStyleSheet(config.CSV_BUTTON_STYLESHEET)
		self.parametersLayout.addWidget(ibetaXtempText)
		self.parametersLayout.addWidget(self.ibetaXtempButton)


		configKeys 	= config.CONFIG_KEYS_SA
		captions	= config.DEFAULT_CAPTIONS_SA
		validators	= config.DEFAULT_VALIDATORS_SA


		for configKey, caption, validator in zip(configKeys, captions, validators):
			self.createEdit(configKey, caption, validator)


	
	def createEdit(self, configKey, caption, validator):

		text = QLabel(caption + ":")
		text.setStyleSheet(config.PARAMETER_STYLESHEET)
		self.edits[configKey] = QLineEdit()
		self.edits[configKey].setStyleSheet(config.PARAMETER_STYLESHEET)
		self.edits[configKey].setAlignment(Qt.AlignRight)

		if validator != config.VALID_ALL:
			self.edits[configKey].setValidator(validator)

		self.parametersLayout.addWidget(text)
		self.parametersLayout.addWidget(self.edits[configKey])



	def keepData(self, data):
		self.data = data
		self.settedData = True



	def saveIBCsvs(self):

		if self.settedData:
			self.timer.stop()

			# Get filenames
			centralIBFilename = QFileDialog.getSaveFileName(None, "Save Central IB Curve CSV.", "", "Central IB Curve (*.csv);;All Files (*)" )
			lateralIBFilename = QFileDialog.getSaveFileName(None, "Save Lateral IB Curve CSV.", "", "Lateral IB Curve (*.csv);;All Files (*)" )


			# If does not want to save anything
			if len(centralIBFilename[0]) == 0 and len(lateralIBFilename) == 0:
				self.settedData = False
				return


			# Arrays to be used by panda to save the csv
			centralIBArray = []
			lateralIBArray = []

			centralIBVector = self.data["central"]
			lateralIBVector = self.data["lateral"]


			# Loop every pair temperature and IB
			for centralTempAndIB, lateralTempAndIB in zip(centralIBVector, lateralIBVector):

				centralIBArray.append({self.edits[config.CONFIG_TEMP_COLUMN_NAME_KEY].text(): centralTempAndIB[0], 
									config.CENTRAL_IB_COLUMN_NAME:  centralTempAndIB[1]})
				
				lateralIBArray.append({self.edits[config.CONFIG_TEMP_COLUMN_NAME_KEY].text(): lateralTempAndIB[0], 
									config.LATERAL_IB_COLUMN_NAME:  lateralTempAndIB[1]})
			

			# Create all dataframes
			dfCentralIB = pd.DataFrame(centralIBArray)
			dfLateralIB = pd.DataFrame(lateralIBArray)


			# Save all dataframes
			if not len(centralIBFilename[0]) == 0:
				dfCentralIB.to_csv(centralIBFilename[0], index=False, encoding='utf-8')
			if not len(lateralIBFilename[0]) == 0:
				dfLateralIB.to_csv(lateralIBFilename[0], index=False, encoding='utf-8')
			
			self.settedData = False



	@Slot(list)
	def save(self):


		# Set status text to SAVING
		self.statusText.setText(config.SAVING_STATUS_TEXT)
		self.statusText.setStyleSheet(config.PROCESSING_STATUS_STYLESHEET)


		variables		= {}


		# Get variables
		# Current Curve Section
		configKeys 		= config.CONFIG_KEYS_CURRENT_CURVE

		intsList		= config.INTEGERS_LIST


		for configKey in configKeys:

			if configKey in intsList:

				variables[ configKey ] = int( self.edits[ configKey ].text() )

			else:

				variables[ configKey ] = float( self.edits[ configKey ].text() )


		# Simulated Annealing
		configKeys 		= config.CONFIG_KEYS_SA

		stringsList		= config.STRINGS_LIST


		for configKey in configKeys:

			if configKey in intsList:

				variables[ configKey ] = int( self.edits[ configKey ].text() )

			elif configKey in stringsList:
			
				variables[ configKey ] = self.edits[ configKey ].text()

			else:

				variables[ configKey ] = float( self.edits[ configKey ].text() )


		# Save to a JSON
		data = {}


		# Hidden Section
		configKeys 		= config.CONFIG_KEYS_HIDDEN


		for configKey in configKeys:
			data[ configKey ] = self.hidden[ configKey ]


		# Current Curve Section
		configKeys 		= config.CONFIG_KEYS_CURRENT_CURVE

		for configKey in configKeys:

			data [ configKey ] = variables[ configKey ]


		# Simulated Annealing
		configKeys 		= config.CONFIG_KEYS_SA

		for configKey in configKeys:

			data [ configKey ] = variables[ configKey ]
		

		self.saveJson(data)


		# Set status text to OK
		self.statusText.setText(config.OK_STATUS_TEXT)
		self.statusText.setStyleSheet(config.OK_STATUS_STYLESHEET)



	def saveJson(self, data):

		# Save data into a JSON
		with open(config.CONFIG_SAVE_NAME, 'w') as outfile:
			json.dump(data, outfile)



	def load(self):


		# Set status text to LOADING
		self.statusText.setText(config.LOADING_STATUS_TEXT)
		self.statusText.setStyleSheet(config.PROCESSING_STATUS_STYLESHEET)


		# Load data from JSON
		data = self.loadJson()

		keys = data.keys()


		# Hidden
		configKeys 		= config.CONFIG_KEYS_HIDDEN
		defaultValues 	= config.DEFAULT_VALUES_HIDDEN


		for configKey, defaultValue in zip(configKeys, defaultValues):
			if configKey in keys:

				self.hidden[configKey] = str( data[ configKey ] )

			else:

				self.hidden[configKey] = str ( defaultValue )



		# Current Curve
		configKeys 		= config.CONFIG_KEYS_CURRENT_CURVE
		defaultValues 	= config.DEFAULT_VALUES_CURRENT_CURVE


		variables		= {}


		for configKey, defaultValue in zip(configKeys, defaultValues):
			if configKey in keys:

				variables[configKey] = str( data[ configKey ] )

			else:

				variables[configKey] = str ( defaultValue )
		


		# Simulated Annealing
		configKeys 		= config.CONFIG_KEYS_SA
		defaultValues 	= config.DEFAULT_VALUES_SA


		for configKey, defaultValue in zip(configKeys, defaultValues):
			if configKey in keys:

				variables[configKey] = str( data[ configKey ] )

			else:

				variables[configKey] = str ( defaultValue )



		# Load data into variables
		# Current Curve
		configKeys 		= config.CONFIG_KEYS_CURRENT_CURVE

		for configKey in configKeys:
			self.edits[configKey].setText( variables[configKey] )


		# Simulated Annealing
		configKeys 		= config.CONFIG_KEYS_SA
		
		for configKey in configKeys:
			self.edits[configKey].setText( variables[configKey] )


		# Set status text to OK
		self.statusText.setText(config.OK_STATUS_TEXT)
		self.statusText.setStyleSheet(config.OK_STATUS_STYLESHEET)



	def loadJson(self):

		# If file does not exist, create it
		jsonFile = Path(config.CONFIG_SAVE_NAME)
		if not jsonFile.is_file():

			data = {}

			# Current Curve
			configKeys 		= config.CONFIG_KEYS_CURRENT_CURVE
			defaultValues 	= config.DEFAULT_VALUES_CURRENT_CURVE

			for configKey, defaultValue in zip(configKeys, defaultValues):
				data [ configKey ] = defaultValue


			# Simulated Annealing
			configKeys 		= config.CONFIG_KEYS_SA
			defaultValues 	= config.DEFAULT_VALUES_SA

			for configKey, defaultValue in zip(configKeys, defaultValues):
				data [ configKey ] = defaultValue


			# Save the new file
			self.saveJson(data)



		# Load data from a JSON
		with open(config.CONFIG_SAVE_NAME) as json_file:
			return json.load(json_file)



	@Slot(list)
	def plotCsvs(self):

		# Get the csv separator
		csvSeparator = self.edits[config.CONFIG_CSV_SEPARATOR_KEY].text()


		if self.igmXtempCsv == "":
			# Set status text to ERROR
			self.statusText.setText(config.ERROR_IGM_X_TEMP_CSV_TEXT)
			self.statusText.setStyleSheet(config.FAILED_STATUS_STYLESHEET)
			self.igmXtempButton.setText(config.CSV_BUTTON_TEXT)

			return
		

		if self.ibetaXtempCsv == "":
			# Set status text to ERROR
			self.statusText.setText(config.ERROR_IBETA_X_TEMP_CSV_TEXT)
			self.statusText.setStyleSheet(config.FAILED_STATUS_STYLESHEET)
			self.ibetaXtempButton.setText(config.CSV_BUTTON_TEXT)

			return

		# Set status text to CALCULATING
		self.statusText.setText(config.CALCULATING_STATUS_TEXT)
		self.statusText.setStyleSheet(config.PROCESSING_STATUS_STYLESHEET)


		self.plotCsvsThread = plotCsvsThread(self.graph, self.statusText, csvSeparator, self.igmXtempCsv, self.ibetaXtempCsv)
		self.plotCsvsThread.start()



	@Slot(list)
	def generateCurrentCorrection(self):


		variables = {}


		# Get variables
		configKeys 		= config.CONFIG_KEYS_SA

		intsList		= config.INTEGERS_LIST
		stringsList		= config.STRINGS_LIST


		for configKey in configKeys:

			if configKey in intsList:

				variables[ configKey ] = int( self.edits[ configKey ].text() )

			elif configKey in stringsList:
			
				variables[ configKey ] = self.edits[ configKey ].text()

			else:

				variables[ configKey ] = float( self.edits[ configKey ].text() )


		# Set status text to CALCULATING
		self.statusText.setText(config.CALCULATING_STATUS_TEXT)
		self.statusText.setStyleSheet(config.PROCESSING_STATUS_STYLESHEET)


		if self.igmXtempCsv == "":
			# Set status text to ERROR
			self.statusText.setText(config.ERROR_IGM_X_TEMP_CSV_TEXT)
			self.statusText.setStyleSheet(config.FAILED_STATUS_STYLESHEET)

			return
		

		if self.ibetaXtempCsv == "":
			# Set status text to ERROR
			self.statusText.setText(config.ERROR_IBETA_X_TEMP_CSV_TEXT)
			self.statusText.setStyleSheet(config.FAILED_STATUS_STYLESHEET)

			return

		# If there is still a thread, terminate it, and stop timer
		try:
			self.timer.stop()
			self.curCorrecThread.do_run = False
		except:
			pass

		self.curCorrecThread 	= currentCorrectionThread(self.graph, self.statusText, variables, self.keepData, self.igmXtempCsv, self.ibetaXtempCsv)
		self.curCorrecThread.daemon = True
		self.curCorrecThread.start()

		# Start a timer to save IB's
		self.timer.start(config.GUI_UPDATE_TIME)
		


	@Slot(list)
	def openigmXtemp(self):

		dialog = QFileDialog(self, directory=self.hidden[ config.CONFIG_IGM_X_TEMP_PATH_KEY ])
		path, _ = dialog.getOpenFileName(caption=config.IGM_X_TEMP_CSV_OPEN_CAPTION , filter="*.csv")
		self.igmXtempCsv = path

		if path != "":
			self.igmXtempButton.setText(config.CSV_OPENED_BUTTON_TEXT)
			self.hidden[ config.CONFIG_IGM_X_TEMP_PATH_KEY ] = path
		else:
			self.igmXtempButton.setText(config.CSV_BUTTON_TEXT)
	


	@Slot(list)
	def openibetaXtemp(self):

		dialog = QFileDialog(self, directory=self.hidden[ config.CONFIG_IBETA_X_TEMP_PATH_KEY ])
		path, _ = dialog.getOpenFileName(caption=config.IBETA_X_TEMP_CSV_OPEN_CAPTION , filter="*.csv")
		self.ibetaXtempCsv = path

		if path != "":
			self.ibetaXtempButton.setText(config.CSV_OPENED_BUTTON_TEXT)
			self.hidden[config.CONFIG_IBETA_X_TEMP_PATH_KEY] = path
		else:
			self.ibetaXtempButton.setText(config.CSV_BUTTON_TEXT)



	@Slot(list)
	def generateCurrentCurve(self):
		
		variables = {}


		# Get variables
		configKeys 		= config.CONFIG_KEYS_CURRENT_CURVE

		intsList		= config.INTEGERS_LIST


		for configKey in configKeys:

			if configKey in intsList:

				variables[ configKey ] = int( self.edits[ configKey ].text() )

			else:

				variables[ configKey ] = float( self.edits[ configKey ].text() )


		# Set status text to CALCULATING
		self.statusText.setText(config.CALCULATING_STATUS_TEXT)
		self.statusText.setStyleSheet(config.PROCESSING_STATUS_STYLESHEET)

		'''
		self.curCurveThread 	= currentCurveThread(self.graph, self.statusText, variables, self.keepData)
		self.curCurveThread.start()
		'''

		# Start a timer to save IB's
		self.timer.timeout.connect(self.saveIBCsvs)
		self.timer.start(config.GUI_UPDATE_TIME)



	def updateStatus(self):

		# Update the status if it is not OK
		if not self.statusText.text() == config.OK_STATUS_TEXT and (type(self.data) is not dict) :
			self.statusText.setText(self.data + config.CALCULATING_STATUS_TEXT)
			self.statusText.setStyleSheet(config.PROCESSING_STATUS_STYLESHEET)
			self.settedData = False
		
		elif isinstance(self.data, curCorrection.current_piecewise):
			
			# Create a dialog
			self.timer.stop()
			dialog = InfoDialog(self.data)
			dialog.exec_()



class InfoDialog(QDialog):
	def __init__(self, curPiecewise):
		QDialog.__init__(self)

		# Set basic parameters of application
		self.setWindowTitle(config.TITLE)
		self.setWindowIcon(QIcon(config.ICON_PATH))
		self.setMaximumWidth(config.MAX_WIDTH_DIALOG)
		self.setStyleSheet(config.BACKGROUND_STYLESHEET)


		# Add the information needed
		text = QLabel(curPiecewise.print_piecewise() + "\nNRMSE: " + str(curPiecewise.energy_cost()))
		text.setStyleSheet(config.DIALOG_TEXT_STYLESHEET)

		closeBtn = QPushButton("Close")
		closeBtn.setStyleSheet(config.CLOSE_BUTTON_STYLESHEET)
		closeBtn.clicked.connect(self.close_dialog)

		layout = QVBoxLayout()
		layout.addWidget(text)
		layout.addWidget(closeBtn)
		self.setLayout(layout)

	

	def close_dialog(self):
		self.done(0)


if __name__ == '__main__':

	# Create the Qt Application
	app = QApplication(sys.argv)

	# Create and show the main application
	main = mainWindow()
	main.show()

	# Run the main Qt loop
	sys.exit(app.exec_())