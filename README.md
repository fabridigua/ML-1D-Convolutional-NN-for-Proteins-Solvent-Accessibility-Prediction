# ML 1D Convolutional NN for Proteins Solvent Accessibility Prediction

This project has been made for Machine Learning Corse at University of Florence.

The Problem
------
The prediction of proteins 3D structure's properties is one of the most popular and studied issue in bioinformatics and Machine Learning.<br>
Nowdays the most frequent approch is using a Recurrent Neural Network (like an LSTM based Model).
Using a Convolutional Neural Network is a good compromision between performance and execution time.
More details in the beamer written presentation.

The Idea
------
Even if the a RNN may capture more distant dependencies between the proteins amino acids, using a CNN will make slightly descend the execution time.
So the idea is using a CNN alone or combining it with a RNN (ispiring from LINK), for capturing both local and gloabal dependencies between the features.

The Project
------
The project, realized with Keras, consists in a sigle ipynb file: you can open it with Google Colab or in you local notebook. Anyway i highly suggest to use a GPU...
There are also many data preprocessing classes and scripts:

The Results
------
The CNN reached 85% of accuracy, while the CNN-LSTM model obtained more than 89% using CullPDB as dataset and training the model in 120 epochs.
