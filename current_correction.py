import time
import numpy
import pandas
import math
import threading
import matplotlib.pyplot as pyplot
from random import uniform, randint, choice



################################# CONSTANTS #################################



# Filepaths related to current x temperature graphs
#IGM_X_TEMP_FILEPATH 	= "filepath/to/Igm_x_Temp"		# The filepath to Igm x Temp
#IBETA_X_TEMP_FILEPATH 	= "filepath/to/Ibeta_x_Temp"	# The filepath to Ibeta x Temp (Iin x Temp)
#IGM_X_TEMP_FILEPATH 	= "csv/Igm_X_T-IC-0.01.csv"		# The filepath to Igm x Temp
#IBETA_X_TEMP_FILEPATH 	= "csv/Ibeta_X_T.csv"			# The filepath to Ibeta x Temp (Iin x Temp)


# Current Piecewise Constants
MAX_MB					= 10							# Maximum multiplier for transistor B
MAX_MC					= 20							# Maximum multiplier for transistor C
MAX_MD					= 20							# Maximum multiplier for transistor D

FULL_RANDOM				= False							# If Ma, Mb, Mc and Md must be picked by random or just Ma and Mb

FIXED_I0				= True							# If I0 current is fixed
I0_AS_IGM_MIN			= True							# If I0 must be equal to the minimum of Igm
I0_VALUE				= 8.567e-6						# Value of I0, if FIXED_I0 = True and I0_AS_IGM_MIN = False

DELTA_I0				= 0.5							# How much I0 can deviate from it's limits in percent


# Simulated Annealing Constants
KB 						= 0.1							# Boltzmann Constant in J * K^-1
INITIAL_TEMPERATURE		= 50							# Initial Temperature in K
FINAL_TEMPERATURE		= 0.01							# Final Temperature to stop Simulated Annealing
COOLING_RATE			= 0.01							# Coefficient for the Temperature drop
MAX_ITERATIONS			= 100							# Maximum number of iterations in Simulated Annealing


# Configurations for running the Simulated Annealing
NUMBER_OF_RECTS			= 3								# Equals to the number of M - 1


# Configurations for csv
#pandas.set_option('precision', 12)						# Precision of the tables to be imported

SEPARATOR				= ';'							# The separator for the csv

TEMPERATURE_COLUMN_NAME = "Temperature"					# The name of the temperature column in the csv file
IGM_COLUMN_NAME 		= "Igm"							# The name of the Igm column in the csv file
IBETA_COLUMN_NAME 		= "Ibeta"						# The name of the Ibeta (Iin) column in the csv file


# Configuration for interpolation
INTERPOLATION_METHOD	= 'linear'						# Linear Interpolation


ACCEPTED_LOWER_ENERGY	= "A_LE"						# If the new Piecewise curve was accepted by lower energy
ACCEPTED_PROBABILITY	= "A_PROB"						# If the new Piecewise curve was accepted by probability



############################ SIMULATED ANNEALING ############################



# Object that keeps the parameters to build the current curve
# Values of Ma, Mb, Mc , Md, must be passed as Ma1=10, Ma2=7, Mc1=3, Md3=8....
class current_piecewise:


	# Initial configuration
	# Not necessary, but is visualy better
	number_rects	= 0							# Quantity of rects

	current_curve	= []#igm_x_ibeta_numpy			# The curve to compare with 

	I0 				= 0							# Constant Source Current
	deltaI0			= 0							# How much I0 can deviate from it's limits
	deltaIB			= 0							# How much IB can deviate from it's limits

	Ma				= []						# Ma values of the transistors
	Mb				= []						# Mb values of the transistors
	Mc				= []						# Mc values of the transistors
	Md				= []						# Md values of the transistors

	max_Mb			= MAX_MB					# Maximum value for Mb multiplier of the transistors
	max_Mc			= MAX_MC					# Maximum value for Mc multiplier of the transistors
	max_Md			= MAX_MD					# Maximum value for Md multiplier of the transistors

	minimum_I0		= 0							# Inferior limit for I0
	maximum_I0		= 0							# Superior limit for I0

	inclination		= []						# If the rects has a positive or negative inclination, must be -1 or 1

	fixed_I0		= FIXED_I0					# If the I0 is fixed
	I0_as_igm_min	= I0_AS_IGM_MIN				# If I0 must be the minimum value of Igm



	# Set each current rect
	def __init__ (self, num_rect, current_curve, I0 = I0_VALUE, deltaI0 = DELTA_I0, max_Mb = MAX_MB, max_Mc = MAX_MC, max_Md = MAX_MD,
				  minimum_I0 = 0, maximum_I0 = 0, fixed_I0 = FIXED_I0, I0_as_igm_min = I0_AS_IGM_MIN, **kwargs):
		
		# Check if the number of rects is smaller than 0
		if num_rect < 0:
			raise Exception ("Number of rects cannot be negative!")


		self.current_curve = current_curve

		
		# Check if kwargs is even and 5 * num_rect or there is no args, 
		# because each rect contains the Ma, Mb, Mc, Md multipliers and the inclination values
		if ((len(kwargs.keys()) != 5 * num_rect) and (len(kwargs.keys()) != 0)):
			raise Exception ("Kwargs must be 4 * num_rect, it should have Ma, Mb, Mc, Md for each rect!")


		if ((self.max_Mb <= 0) or (self.max_Mc <= 0) or (self.max_Md < 0)):
			raise Exception ("The maximum multiplier must be greater than 0, and for Md, must be at least 0!")
		

		# Set the limits
		self.max_Mb 			= max_Mb
		self.max_Mc 			= max_Mc
		self.max_Md 			= max_Md

		self.deltaI0			= deltaI0
		self.fixed_I0			= fixed_I0


		ibeta_min, ibeta_max, igm_min, igm_max, _, _ = self.__current_curve_get_limits__ ()


		# I0 Minimum
		if (minimum_I0 == 0):
			self.minimum_I0	= igm_min - (igm_max - igm_min)*deltaI0
		
		else:
			self.minimum_I0	= minimum_I0
		

		# I0 Maximum
		if (maximum_I0 == 0):
			self.maximum_I0	= igm_max + (igm_max - igm_min)*deltaI0
		
		else:
			self.maximum_I0	= maximum_I0


		# Set the other variables
		self.number_rects = num_rect

		if (I0_as_igm_min == True):

			self.I0 = self.current_curve[0][0]
			self.I0_as_igm_min = True

		else:

			self.I0 = I0
			self.I0_as_igm_min = False

		self.IB = ibeta_min


		# If args are not passed, make it random
		if (len(kwargs.keys()) == 0):
			self.pick_random()


		else:

			# Iterate the kwargs and populate Ma, Mb, Mc and Md
			for iterator in range (0, self.number_rects):
				
				Ma 				= kwargs.get ('Ma' + str(iterator))
				Mb 				= kwargs.get ('Mb' + str(iterator))
				Mc 				= kwargs.get ('Mc' + str(iterator))
				Md 				= kwargs.get ('Md' + str(iterator))
				inclination		= kwargs.get ('inclination' + str(iterator))

				# If any does not exists
				if ((not Ma) or (not Mb) or (not Mc) or (not Md) or (not inclination)):
					raise Exception ("Some values of the rect " + str(iterator) + " are missing!")
				
				self.Ma.append (Ma)
				self.Mb.append (Mb)
				self.Mc.append (Mc)
				self.Md.append (Md)


				# Check the inclination
				if ((inclination != -1) or (inclination != 1)):
					raise Exception ("Inclination must be -1 or 1!")

				self.inclination.append (inclination)
	



	def __current_curve_get_limits__ (self):

		ibeta_max 	= 0
		ibeta_min 	= 100
		igm_max		= 0
		igm_min		= 100

		for current_point in self.current_curve:
			# [0] = Igm
			# [1] = Ibeta

			if (current_point[1] > ibeta_max):

				ibeta_max = current_point[1]

			if (current_point[1] < ibeta_min):

				ibeta_min = current_point[1]
			

			if (current_point[0] > igm_max):

				igm_max = current_point[0]

			if (current_point[0] < igm_min):

				igm_min = current_point[0]
		

		igm_last   = self.current_curve[-1][0]
		ibeta_last = self.current_curve[-1][1]

		# Return the maximum and minimum 
		return (ibeta_min, ibeta_max, igm_min, igm_max, ibeta_last, igm_last)
	


	# Turn alphas and start_points into random numbers
	def pick_random (self):

		# Reset arrays
		self.Ma				= []
		self.Mb				= []
		self.Mc				= []
		self.Md				= []
		self.inclination	= []


		# Set a random value for I0 and IB
		if (self.fixed_I0 == False):
			self.I0 = uniform (self.minimum_I0, self.maximum_I0)


		# Get the limits for Ma
		ibeta_min, ibeta_max, _, _, ibeta_last, igm_last = self.__current_curve_get_limits__ ()


		# Fill arrays
		if (FULL_RANDOM == True):

			for iterator in range (0, self.number_rects):
			
			
				self.Mb.append (randint (1, self.max_Mb))


				# Calculate the limits for Ma
				Ma_min = math.ceil ((ibeta_min / ibeta_max) * self.Mb[iterator])
				Ma_max = self.Mb[iterator]
				
				self.Ma.append (randint (Ma_min, Ma_max))



				self.Mc.append (randint (1, self.max_Mc))
				self.Md.append (randint (0, self.max_Md))		# The segment/rect can have a 0 coefficient (Constant)


				self.inclination.append (numpy.random.choice ([-1, 1]))			# It's an uniform distribution
		

		else:

			Mb = randint (1, self.max_Mb)


			# Calculate the limits for Ma
			Ma_min = math.ceil ((ibeta_min / ibeta_max) * Mb)
			Ma_max = Mb
				
			Ma = randint (Ma_min, Ma_max)


			Ix_done = []
			last_Ix = (Mb/Ma)*self.IB
			Ix_done.append (last_Ix)


			# Add the rest all Ix's to be done
			for iterator in range (1, self.number_rects):

				# Loop until find a possibility that was not done yet
				while last_Ix in Ix_done:

					Mb = randint (1, self.max_Mb)


					# Calculate the limits for Ma
					Ma_min = math.ceil ((ibeta_min / ibeta_max) * Mb)
					Ma_max = Mb
				
					Ma = randint (Ma_min, Ma_max)

					# Choose a new Ix to be done
					last_Ix = (Mb/Ma)*self.IB
				

				Ix_done.append (last_Ix)
			

			# Sort the list
			Ix_done.sort ()


			# Check for each Ma and Mb possibility and find the best
			for iterator in range (0, len(Ix_done)):
				best_Ma = 1
				best_Mb = 1

				best_error = 1000

				for Mb in range (1, self.max_Mb + 1):

					for Ma in range (math.ceil ((ibeta_min / ibeta_max) * Mb), Mb + 1):

						if (abs((Ix_done[iterator]) - (Mb/Ma)*self.IB) < best_error):
							best_Ma = Ma
							best_Mb = Mb
							best_error = abs((Ix_done[iterator]) - (Mb/Ma)*self.IB)
			
				self.Ma.append (best_Ma)
				self.Mb.append (best_Mb)
				Ix_done[iterator] = (self.Mb[iterator]/self.Ma[iterator])*self.IB


			# Save auxiliary information
			igm_values 			= []
			inclination_values 	= []


			# Find all Igm's and get the inclination
			for Ix in Ix_done:

				# Find the nearest Igm and append
				_, igm = self.__find_nearest_igm__(Ix)

				igm_values.append (igm)

			
			# Adds the last Ibeta and Igm
			Ix_done.append (ibeta_last)
			igm_values.append (igm_last)


			# Remove the I0 for the first Igm
			#igm_values[0] -= self.I0
			

			# Fill the inclination values
			for iterator in range (0, len(igm_values) - 1):

				igm_values [iterator] = self.current_point_value (Ix_done[iterator], iterator)
				igm_values [iterator + 1] = igm_values [iterator + 1] - self.current_point_value (Ix_done[iterator + 1], iterator)


				# Calculates deltaY / deltaX
				inclination_values.append ((igm_values[iterator + 1]) / (Ix_done[iterator + 1] - Ix_done[iterator]))


				# Check every Mc and Md and find the best
				best_Mc = 1
				best_Md = 0

				best_error = 1000

				for Mc in range (1, self.max_Mc + 1):

					for Md in range (0, self.max_Md + 1):

						if (abs((Md/Mc) - abs(inclination_values[iterator])) < best_error):
							best_Mc = Mc
							best_Md = Md
							best_error = abs((Md/Mc) - abs(inclination_values[iterator]))
				
				self.Mc.append (best_Mc)
				self.Md.append (best_Md)


				# Append the value of inclination
				if (inclination_values[iterator] >= 0):

					self.inclination.append (1)

				else:

					self.inclination.append (-1)
				

				#igm_values [iterator] = self.current_point_value (Ix_done[iterator], iterator + 1)



	# Finds the nearest Igm, returns the position in the current_curve and the value of Igm
	def __find_nearest_igm__ (self, ibeta):

		# Make an array to save all Igm's
		ibeta_curve = []


		# Fill igm_curve
		for current_point in self.current_curve:
			# [0] = Igm
			# [1] = Ibeta

			ibeta_curve.append (current_point[1])

		# Get the nearest
		position = (numpy.abs(ibeta_curve - ibeta)).argmin()
		nearest_igm = self.current_curve[position][0]

		return (position, nearest_igm)



	# Return the Normalized RMSE of the curve
	def energy_cost (self):

		mse = 0
		n = 0

		ymax = 0
		ymin = 100


		for current_point in self.current_curve:
			# [0] = Igm
			# [1] = Ibeta

			mse += (self.current_point_value(current_point[1], self.number_rects) - current_point[0]) ** 2

			if (current_point[0] > ymax):

				ymax = current_point[0]

			if (current_point[0] < ymin):

				ymin = current_point[0]

			# Increment the quantity of elements
			n += 1

		mse = mse/n

		# Return the NRMSE
		return (numpy.sqrt(mse))/(ymax - ymin)
	


	# Prints the Current Piecewise
	def print_piecewise (self):

		text  = "I0:\t\t" + str(self.I0) + "\n"
		text += "IB:\t\t" + str(self.IB) + "\n\n"

		for iterator in range (0, self.number_rects):

			text += "Rect " + str(iterator) + ":\n"

			text += "Ma:\t\t" + str(self.Ma[iterator]) + "\n"
			text += "Mb:\t\t" + str(self.Mb[iterator]) + "\n"
			text += "Mc:\t\t" + str(self.Mc[iterator]) + "\n"
			text += "Md:\t\t" + str(self.Md[iterator]) + "\n"
			text += "inclination:\t" + str(self.inclination[iterator]) + "\n\n"
		
		print (text)

		return text
	


	# Returns the value of the current given Ibeta (Iin)
	def current_point_value (self, ibeta, num_rects):

		current_value = self.I0

		for iterator in range (0, num_rects):

			# IPCW = I0 + sum mi * (Iin - Ixi) * u (Iin - Ixi)
			# mi = inclinationi * Mdi/Mci, where inclinationi is -1 or 1
			# Ixi = (Mbi/Mai) * IB
			mi = (self.inclination[iterator] * self.Md[iterator])/self.Mc[iterator]
			Ixi = (self.Mb[iterator] / self.Ma[iterator]) * self.IB
			current_value += mi * (ibeta - Ixi) * numpy.heaviside(ibeta - Ixi, 1)

		return current_value
	


	# Auxiliary function to help plotting the curve
	def plot (self, x_axis):
		
		y_axis = []

		for x_value in x_axis:

			y_axis.append(self.current_point_value (x_value, self.number_rects))
		
		return y_axis

	


class simulated_annealing:


	# Set variables and initial points
	def __init__ (self, initial_config, initial_temp = INITIAL_TEMPERATURE, final_temp = FINAL_TEMPERATURE, max_iter = MAX_ITERATIONS, kb = KB, cooling_rate = COOLING_RATE):

		# Check for errors
		if (final_temp >= initial_temp):
			raise Exception ("The final temperature must be smaller than the initial temperature!")


		if (max_iter <= 0):
			raise Exception ("Max Iterations must be positive and bigger than 0!")

		
		if (kb == 0):
			raise Exception ("kb cannot be 0!")


		if ((cooling_rate <= 0) or (cooling_rate >= 1)):
			raise Exception ("Cooling rate must be in the interval: ]0, 1[!")
		

		# Set the values
		self.initial_configuration 		= initial_config
		#self.igm_x_ibeta				= igm_x_ibeta
		self.temperature 				= initial_temp
		self.final_temperature 			= final_temp
		self.maximum_iterations 		= max_iter
		self.kb							= kb
		self.cooling_rate				= cooling_rate



	# Returns the probability of accepting the new step
	def __acceptance_probability__ (self, energy, new_energy, temperature, kb):

		if (new_energy < energy):
			return 1.0, ACCEPTED_LOWER_ENERGY

		return numpy.exp ((energy - new_energy) / (kb * temperature)), ACCEPTED_PROBABILITY
	


	# Reduces the temperature
	def __cool_temperature__ (self, temperature, cooling_rate, final_temp):
		temperature = temperature * (1 - cooling_rate)

		if (temperature < final_temp):
			temperature = final_temp

		return temperature
	


	def run (self, updateStatusFunc):

		best = self.initial_configuration
		best_energy = self.initial_configuration.energy_cost()
		counter = 0

		thread = threading.currentThread()
		

		while (self.temperature > self.final_temperature) and (getattr(thread, "do_run", True)):

			# Check if need to quit
			#try:
			#	thread = threading.currentThread()
			#	if getattr(thread, "do_run", True):
			#		return

			#except:
			#	pass

			# Update Status in percentage
			status = "[ " + "{:.2f}".format(self.temperature) + "C / " + "{:.2f}".format(self.final_temperature) + "C ]"
			updateStatusFunc(status)

			# Put the Thread to sleep if counted more than 20 times
			# Simple fix to Python's thread problem
			if counter >= 20:
				time.sleep(1)
				counter = 0
			else:
				counter += 1


			num_prob_accepted = 0											# Number of accepted by probability
			num_lowe_accepted = 0											# Number of accepted by lower energy

			for _ in range (0, self.maximum_iterations):

				# Create a new piecewise current class
				random_current_pcw = current_piecewise (self.initial_configuration.number_rects, self.initial_configuration.current_curve,
													I0=self.initial_configuration.I0, fixed_I0=self.initial_configuration.fixed_I0, I0_as_igm_min=self.initial_configuration.I0_as_igm_min,
													deltaI0=self.initial_configuration.deltaI0, max_Mb=self.initial_configuration.max_Mb, 
													max_Mc=self.initial_configuration.max_Mc, max_Md=self.initial_configuration.max_Md,
				  									minimum_I0=self.initial_configuration.minimum_I0, maximum_I0=self.initial_configuration.maximum_I0)

				# Choose a new random values
				#random_current_pcw.pick_random()							# It is already done when calling current_piecewise with no Ma, Mb, Mc and Md


				# Calculate the energy
				energy = self.initial_configuration.energy_cost()
				new_energy = random_current_pcw.energy_cost()


				# Get the acceptance probability
				acceptance, accepted_by = self.__acceptance_probability__ (energy, new_energy, self.temperature, self.kb)


				# Best globally
				if ((accepted_by == ACCEPTED_LOWER_ENERGY) and (new_energy < best_energy)):
					best = random_current_pcw
					best_energy = new_energy

					print("\n")
					print("New Best:\n")
					best.print_piecewise()
					print("\nNRMSE: " + str(best.energy_cost()))


				# If it is accepted, change values
				if ((accepted_by == ACCEPTED_LOWER_ENERGY) or ((accepted_by == ACCEPTED_PROBABILITY) and (acceptance >= uniform (0, 1) ))):

					self.initial_configuration = random_current_pcw


					if   (accepted_by == ACCEPTED_LOWER_ENERGY):
						num_lowe_accepted += 1
					
					elif (accepted_by == ACCEPTED_PROBABILITY):
						num_prob_accepted += 1



			self.temperature = self.__cool_temperature__(self.temperature, self.cooling_rate, self.final_temperature)


			print ("Accepted by Probability:      " + str(num_prob_accepted) + "/" + str(self.maximum_iterations))
			print ("Accepted by Lower Energy:     " + str(num_lowe_accepted) + "/" + str(self.maximum_iterations))
			print ("NRMSE:     " + str(best.energy_cost()))
			print ("\n\nTemperature:     " + str(self.temperature))


		return best