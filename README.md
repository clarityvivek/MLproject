## End to end machine learning project
Layer 1: notebook/ - The Lab Bench
"Before you build a rocket, you first play with model rockets."
- EDA.ipynb: You explore the data. Are there missing values?
- MODEL TRAINING.ipynb: You train some models manually, try a few algorithms, and see what works.
Goal: Build your understanding and logic here, before automating anything.


Layer 2: src/components/ - The Parts Factory
"Every ML system is a combination of repeatable components."
- data_ingestion.py: Reads data from a file or database.
- data_transformation.py: Scales, encodes, and transforms data.
- model_trainer.py: Trains the ML model and returns it.
- __init__.py: Makes this folder a Python module.
Think of this folder like building engines, tires, and fuel tanks - not the full car, just parts.


Layer 3: src/pipeline/ - The Assembly Line
"What good are parts if they don't come together and run on their own?"
- train_pipeline.py: Loads data -> transforms it -> trains model -> saves it.
- predict_pipeline.py: Loads the model -> takes input -> returns prediction.
The pipeline automates everything you were doing manually in the notebook.


Layer 4: Tools - Your Toolbox
"To build stable systems, you need diagnostics and utilities."
- logger.py: Logs errors, progress, and messages.
- exception.py: Custom error messages that help trace bugs.
- utils.py: Miscellaneous tools.
These make your system reliable.


Layer 5: Project Meta - Packaging and Environment
"A model isn't useful unless it can be shared, installed, and run."
- requirements.txt: List of libraries.
- setup.py + pyproject.toml: Turns your code into an installable Python package.
- .gitignore: Tells Git to ignore junk.
- venv/: Your private environment.
Final Form: ML Project as a Product
You're not just training a model. You're building a machine that others can run safely and repeatedly.
This structure lets you:
- Train new models on new data automatically.
- Make predictions consistently.
- Handle errors gracefully.
- Track logs for debugging.
- Share your project as a package.
