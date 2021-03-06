import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

# Function to split data into test and training data
def split_data(csv, train_ratio, random_val, scale=True):
    # Splitting values into results and training data
    result = csv.loc[:,'Outcome']
    data = csv.drop('Outcome', 'columns')
    x_train, x_test, y_train, y_test = train_test_split(data, result, train_size=train_ratio, random_state=random_val)

    if scale:
        # Scaling values
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

    return [x_train, x_test, y_train, y_test]

# Generates neural network and runs fitting and prediction. Returns predictions, confusion matrix, and score
def neural_network(data, hidden_layer_size, activation, solver, max_iter, shuffle = False, random_state = None):
    mlp = MLPClassifier(hidden_layer_size, activation=activation, solver=solver, max_iter=max_iter, shuffle=shuffle, random_state=random_state)
    mlp.fit(data[0], data[2])
    prediction = mlp.predict(data[1])
    return [prediction, confusion_matrix(data[3], prediction), mlp.score(data[1], data[3])]

# Test performance with all optimized values
def final_test(csv):
    # Best activation function and solver combination found
    activation = "identity"
    solver = "lbfgs"
    
    # Test variables
    num_test = 200
    train_ratio = 0.8
    hidden_layer = (6, 6, 6, 6)
    max_iteration = 20
    results = [[], []]

    # Run test
    for test in range(num_test):
        print("Test run {} beginning".format(test+1))
        data = split_data(csv, train_ratio, test, True)
        result = neural_network(data, hidden_layer, activation, solver, max_iteration, False, test)
        results[0].append(result[1])
        results[1].append(result[2])
        print("Test run {} completed\n".format(test+1))
        
    # Compile and print results
    mean_score = sum(results[1])/num_test
    print("Mean Score: {}".format(mean_score))
    print("Summed Confusion Matrix:")
    print(sum(results[0]))

    x = [i for i in range(1,num_test+1)]
    y = results[1]
    plt.figure()
    plt.plot(x,y, "r.--")
                
    plt.title("Final Test")
    plt.ylabel("Score")
    plt.xlabel("Test Run")
    plt.savefig("figures/Final_test/Final result",bbox_inches="tight")
    plt.show()

def main():
    # Reading csv file into dataframe
    csv = pd.read_csv("diabetes.csv")

    # Run test function
    final_test(csv)

if __name__ == "__main__":
    main()
