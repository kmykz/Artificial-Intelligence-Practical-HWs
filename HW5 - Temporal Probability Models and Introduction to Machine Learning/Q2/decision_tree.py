
import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
Name = "Kamyar Kazari"
Student_Number = "99102037"

random.seed(10)


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        """
        Class for storing Decision Tree as a binary-tree
        Inputs:
        - feature: Name of the the feature based on which this node is split
        - threshold: The threshold used for splitting this subtree
        - left: left Child of this node
        - right: Right child of this node
        - value: Predicted value for this node (if it is a leaf node)
        """
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        pass

    def is_leaf(self):
        """
        Returns True if this node is a leaf node
        """
        return self.left is None and self.right is None


class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2):
        """
        Class for implementing Decision Tree
        Attributes:
        - max_depth: int
            The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until
            all leaves contain less than min_samples_split samples.
        - min_num_samples: int
            The minimum number of samples required to split an internal node
        - root: Node
            Root node of the tree; set after calling fit.
        """
        self.root = None
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split

    def is_splitting_finished(self, depth, num_class_labels, num_samples):
        """
        Criteria for continuing or finishing splitting a node
        Inputs:
        - depth: depth of the tree so far
        - num_class_labels: number of unique class labels in the node
        - num_samples: number of samples in the node
        :return: bool
        """
        return depth >= self.max_depth or num_class_labels == 1 or num_samples < self.min_samples_split

    def split(self, X, y, feature, threshold):
        """
        Splitting X and y based on value of feature with respect to threshold;
        i.e., if x_i[feature] <= threshold, x_i and y_i belong to X_left and y_left.
        Inputs:
        - X: Array of shape (N, D) (number of samples and number of features respectively), samples
        - y: Array of shape (N,), labels
        - feature: Name of the the feature based on which split is done
        - threshold: Threshold of splitting
        :return: X_left, X_right, y_left, y_right
        """
        X_left = []
        X_right = []
        y_left = []
        y_right = []
        for i in range(len(X)):
            if X[i][feature] <= threshold:
                X_left.append(X[i])
                y_left.append(y[i])
            else:
                X_right.append(X[i])
                y_right.append(y[i])
        return X_left, X_right, y_left, y_right

    def entropy(self, y):
        """
        Computing entropy of input vector
        - y: Array of shape (N,), labels
        :return: entropy of y
        """
        if len(y) == 0:
            return 0
        p_true = sum(y) / len(y)
        p_false = 1 - p_true
        return -p_true * np.log2(p_true) - p_false * np.log2(p_false)

    def information_gain(self, X, y, feature, threshold):
        """
        Returns information gain of splitting data with feature and threshold.
        Hint! use entropy of y, y_left and y_right.
        """
        entropy_of_data = self.entropy(y)
        X_left, X_right, y_left, y_right = self.split(X, y, feature, threshold)
        entropy_of_left = self.entropy(y_left)
        entropy_of_right = self.entropy(y_right)
        return entropy_of_data - (len(X_left) / len(X)) * entropy_of_left - (len(X_right) / len(X)) * entropy_of_right

    def best_split(self, X, y):
        """
        Used for finding best feature and best threshold for splitting
        Inputs:
        - X: Array of shape (N, D), samples
        - y: Array of shape (N,), labels
        :return:
        """
        best_feature = None
        best_threshold = None
        best_gain = 0
        # todo: You'd better use a random permutation of features 0 to D-1
        features = X[0].keys()
        features = list(features)
        random.shuffle(features)
        for feature in features:
            thresholds = [X[i][feature] for i in range(len(X))]
            # todo: use unique values in this feature as candidates for best threshold
            for threshold in thresholds:
                gain = self.information_gain(X, y, feature, threshold)
                if gain > best_gain:
                    best_feature = feature
                    best_threshold = threshold
                    best_gain = gain
        return best_feature, best_threshold

    def build_tree(self, X, y, depth=0):
        """
        Recursive function for building Decision Tree.
        - X: Array of shape (N, D), samples
        - y: Array of shape (N,), labels
        - depth: depth of tree so far
        :return: root node of subtree
        """
        current_node = Node()
        if not self.is_splitting_finished(depth, len(np.unique(y)), len(y)):
            best_feature, best_threshold = self.best_split(X, y)
            if best_feature == None:
                current_node.value = np.unique(y)[np.argmax(np.bincount(y))]
                return current_node
            X_left, X_right, y_left, y_right = self.split(
                X, y, best_feature, best_threshold)
            current_node.feature = best_feature
            current_node.threshold = best_threshold
            current_node.left = self.build_tree(X_left, y_left, depth + 1)
            current_node.right = self.build_tree(X_right, y_right, depth + 1)
        else:
            current_node.value = np.unique(y)[np.argmax(np.bincount(y))]
        return current_node

    def fit(self, X, y):
        """
        Builds Decision Tree and sets root node
        - X: Array of shape (N, D), samples
        - y: Array of shape (N,), labels
        """
        self.root = self.build_tree(X, y)

    def predict(self, X):
        """
        Returns predicted labels for samples in X.
        :param X: Array of shape (N, D), samples
        :return: predicted labels
        """
        labels = []
        for sample in X:
            current_node = self.root
            while not current_node.is_leaf():
                if sample[current_node.feature] <= current_node.threshold:
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            labels.append(current_node.value)
        return labels


# import data
df = pd.read_csv('breast_cancer.csv')
X_train, X_validation, y_train, y_validation = train_test_split(
    df.drop('target', axis=1), df['target'], test_size=0.2, random_state=42)
X_validation = X_validation.to_dict(orient='records')
X_train = X_train.to_dict(orient='records')
y_validation = y_validation.to_numpy()
y_train = y_train.to_numpy()
tree_depth = 0
tree_split_min = 0
accuracy = 0
for i in range(5):
    for j in range(5):
        tree = DecisionTree(max_depth=i, min_samples_split=j)
        tree.fit(X_train, y_train)
        y_pred = tree.predict(X_validation)
        new_accuracy = sum(a == b for a, b in zip(
            y_validation, y_pred)) / len(y_validation)
        if new_accuracy > accuracy:
            accuracy = new_accuracy
            tree_depth = i
            tree_split_min = j
tree = DecisionTree(max_depth=tree_depth, min_samples_split=tree_split_min)
tree.fit(X_train, y_train)
df2 = pd.read_csv('test.csv')
X_test = df2.to_dict(orient='records')
y_res = tree.predict(X_test)
y_res = pd.DataFrame(y_res, columns=['target'])
y_res.to_csv('output.csv', index=False)


# Split your data to train and validation sets

# Tune your hyper-parameters using validation set

# Train your model with hyper-parameters that works best on validation set

# Predict test set's labels
