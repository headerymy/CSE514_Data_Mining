First of all you should open all files inside the ¡°Decision Tree & Random Forest¡± folder in Python complier like Pycharm. All files are randiomforest, decisiontree, treenode and dataset. Then chose python 3.5 as your interpreter.


DECISION TREE
Compute the Entropy of the final class and after split. Then get the information gain. Use max info gain to split the variable. Meanwhile also need to get the label for each attribute. The main step is to build the tree. Use max gain, attribute label and tree node function to split the data and also decide where to stop.1. The test and training data should be put in the ¡°data¡± folder.
2. The first row in CSV file should be attribute.
3. (If you changed the training and test file name)Before you run the program, you should change the file name in Line 239 for the training data file and in Line 248 for the test data file in ¡°decisiontree.py¡±.
4. Click run inside decisiontree.py file.
5. The result contains only the classes for test data and the final result accuracy.


RANDOM FOREST
Basically same as the decision tree. I just add a function the split the dataset into several parts with specific percentage. The number of parts and the percentage can be manually modified in the program. Then use decision tree to each sub-dataset. We will get several different result sets. Then I add a majority vote module to combine the subsets result to final result.  

1. The test and training data should be put in the ¡°data¡± folder.
2. The first row in CSV file should be attribute.
3. (If you changed the training and test file name)Before you run the program, you should change the file name in Line 93 for the training data file and in Line 115 for the test data file.
4. Click run inside randomforest.py file.
5. The result contains only the classes for test data and the final result accuracy.