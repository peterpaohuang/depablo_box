import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import ast
import re
import cPickle

from utils import calculate_descriptor

# test different image backends
gui_env = ['TKAgg','GTKAgg','Qt4Agg','WXAgg']
for gui in gui_env:
    try:
        print "testing", gui
        matplotlib.use(gui,warn=False, force=True)
        from matplotlib import pyplot as plt
        break
    except:
        continue

import seaborn as sns

class PDBML:
	def __init__(self):
		self.df = pd.read_csv('polymer_db.csv')
		self.set_index("polymer_name", inplace=True) 
		# set index as polymer name rather than integer - each name is unique

		self.pd = pd

	def get_descriptors(chemical_name, descriptor_list):
		"""
		Generate properties for single chemical 

		Parameters
		------------------------
		chemical_name: String
			Unique name of chemical

		descriptor_list: [String]
			List of descriptors

		Returns
		-------------------------
		single_row_df: DataFrame
			one chemical dataframe with each column representing a generated descriptor based on descriptor_list

		"""

		smiles = self.df["smiles"]["chemical_name"]

		single_row_df = pd.DataFrame()
		for descriptor in descriptor_list:
			single_row_df[descriptor] = calculate_descriptor(smiles, descriptor)

		# set index of new dataframe as the unique name of chemical
		single_row_df.set_index([pd.Index([chemical_name])], inplace=True)

		return single_row_df

	def add_descriptors(descriptor_list):
		"""
		Generate column of descriptor values for each descriptor in descriptor_list and append to DataFrame

		Parameters
		-------------------------
		descriptor_list: [String]
			List of descriptors


		Returns
		-------------------------
		None

		"""

		for descriptor in descriptor_list:
			if descriptor not in list(self.df):
				generated_descriptor_series = self.df["smiles"].apply(calculate_descriptor, args=(descriptor))

				#store generated descriptor series in class df
				self.df[descriptor] = generated_descriptor_series

	def property_existence(property_list):
		"""
		Check if each property in property_list exists in dataframe
		If not, create new column and store property values for missing property column into class dataframe

		Parameters
		-------------------------
		property_list: [String]
			List of properties


		Returns
		-------------------------
		None
		"""

		for prop in property_list:
			if prop not in property_list.columns:
				add_descriptors([prop])

	def plot_properties(property_x=None, property_y=None):
		"""
		Plot a scatterplot of two properties against each other

		Parameters
		-------------------------
		property_x: String
			property on x-axis
		property_y: String
			property on y-axis

		Returns
		-------------------------
		Scatter plot on pyplot	
		"""

		property_existence([property_x, property_y])

		self.df.plot(kind='scatter',x=property_x,y=property_y,color='red')
		plt.show()

	def plot_many(property_list):
		"""
		Plot a pairplot of property_list

		Parameters
		-------------------------
		property_list: [String]
			list of properties

		Returns
		-------------------------
		Pairplot on pyplot	
		"""

		sns.pairplot(self.df)
		plt.show()

	def property_correlation(property_1, property_2):
		"""
		Calculate correlation between two properties based on Pearson correlation

		Parameters
		-------------------------
		property_1: String
		property_2: String

		Returns
		-------------------------
		correlation: Float

		"""

		property_existence([property_1, property_2])
		correlation = self.df[property_1].corr(self.df[property_2])

		return correlation

	def correlation_map(property_list):
		"""
		Plot a correlation heatmap of property_list based on Pearson correlation

		Parameters
		-------------------------
		property_list: [String]
			list of properties

		Returns
		-------------------------
		Correlation heatmap on pyplot	
		"""

		corr = self.df[property_list].corr()
		sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True), annot=True)
		plt.show()

	def export_csv(outpath):
		"""
		Export current class dataframe to a csv file

		Parameters
		-------------------------
		outpath: String
			file path to write csv file to

		Returns
		-------------------------
		csv file created in given outpath
		"""

		self.df.to_csv(outpath)

	def train_prediction_model(input_properties, output_property):
		"""
		Train a regression model based on input_properties to predict output_property

		Parameters
		-------------------------
		input_properties: [String]
			list of properties user wants to have as features for model
		output_property: String
			single property user wants to predict

		Returns
		-------------------------
		fitted_model: Sklearn fitted model, ready for prediction
		"""

		pass
	def predict():
		pass
	def export_fitted_model():
		pass


