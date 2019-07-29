# Depablo_Box

## Requirements

1. Conda is installed

## Installation
1. `git clone https://github.com/peterpaohuang/depablo_box.git`
2. `conda create -c rdkit -n depablo_box_env rdkit`
3. `conda activate depablo_box_env`
4. Download [polymer_db.csv](https://drive.google.com/file/d/1J0MbhEI2AIuihl0YavBBL0xl9xWgDBjQ/view?usp=sharing)
5. Move polymer_db.csv into depablo_box directory
6. `python setup.py` while inside depablo_box_env conda environment

## Initialize
```
from depablo_box import PDBML, model

dx = PDBML()
```
## Understand the database
### Access database as pandas dataframe
```
df = dx.df
```

### List all polymers and corresponding smiles
```
# list both polymer names and smiles
df[["Polymer Name", "SMILES"]]

# list only polymer names
df["Polymer Name"]

# list only smiles
df["SMILES"]

# retrieve polymer row by polymer_name
df.loc[df["Polymer Name"] == polymer_name]

# retrieve polymer row by smiles
df.loc[df["SMILES"] == smiles]
```

### List Descriptors
```
dx.chemical_descriptors
dx.experimental_descriptors
```

### List Machine Learning Methods
```
dx.ml_methods
```

## How to use
_Note: currently, depablo_box is only able to handle the calculation of chemical descriptors. Experimental descriptors already exists within the database (dx.df)_
### Get Chemical Descriptors 
```
descriptor_list = ["ExactMolWt", "HeavyAtomMolWt"]
descriptor_df = dx.get_descriptors("Polyethylene", descriptor_list)
```

### Generate Input Files for Quantum Chemistry Codes
```
polymer_identifier = '*C(C*)C'
conversion_format = 'Gaussian 98/03 Input'
outpath = '/file/path/your_polymer.xyz'
dx.create_input_file(polymer_identifier, conversion_format, outpath)
```

### Add Chemical Descriptors to dataframe
```
dx.add_descriptors(descriptor_list)
```
### Plot Properties as scatterplot
```
dx.plot_properties(property_x="Tg", property_y="ExactMolWt")
```
### Plot Many Properties as Pairplot
```
dx.plot_many(property_list)
```
### Get Correlation Between Two Properties
```
dx.property_correlation("Tm", "HeavyAtomMolWt")
```
### Plot Correlation Heatmap of Many Properties
```
dx.correlation_map(property_list)
```
### Export Dataframe as CSV file
```
dx.export_csv(outpath)
```
## Initialize Model Training
```
# input_properties must have already been added to PDBML().df
input_properties = ["Tm", "ExactMolWt", "HeavyAtomMolWt"]
output_property = "Tg"
na_strategy = "mean"
ml = model(df, input_properties, output_property, na_strategy=na_strategy)
```
### Train Model
#### Model Types
1. `Support Vector Regression`
2. `Linear Regression`
3. `Ridge Regression`
4. `Lasso Regression`
5. `Gaussian Process Regression`
```
model_type = "Support Vector Regression"
ml.train(model_type)
```
#### View Trained Model R^2 Score
```
ml.r_2
```

### Predict on new data
```
new_data = [["10.5", "29", "102.1"]]
results = ml.predict(new_data)
```
### Plot Feature Importances
_Note: model type Gaussian Process Regression does not support feature importances_
```
ml.feature_importances()
```
### Export Trained Model as Pickle File
```
ml.export_fitted_model(outpath)
```
### Load Pickle File as Trained Model
```
import pickle
ml = pickle.load(outpath)
results = ml.predict(new_data)
```
## Scrape PolyInfo for experimental properties
```

```
