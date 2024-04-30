# Need to create a window that shows 2 images, asks questions, stores answers in dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC


def trainImageData(df_dir):
    data = pd.read_csv(df_dir)

    y = data['change']  # Labels
    X = data[['img', 'building_percent', 'overlap_percent']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)  # 90% training

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("RF Accuracy: "+str(accuracy_score(y_test, y_pred)))


    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    # Saving model
    #joblib.dump(knn, 'best_model.pkl')  # Save model as pkl file
    print("KNN Accuracy: "+str(accuracy_score(y_test, y_pred)))


    DT = DecisionTreeClassifier()
    DT.fit(X_train, y_train)
    y_pred =DT.predict(X_test)
    print("DT Accuracy: "+str(accuracy_score(y_test, y_pred)))


    sgdc = SGDClassifier(max_iter=100, tol=0.01)
    sgdc.fit(X_train, y_train)
    y_pred = sgdc.predict(X_test)
    print("SGDC Accuracy: "+str(accuracy_score(y_test, y_pred)))


    # Import svm model
    from sklearn import svm
    clf = svm.SVC(kernel='poly')  # Linear Kernel
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("SVM Accuracy: "+str(accuracy_score(y_test, y_pred)))



if __name__ == "__main__":
    trainImageData("./files/trainingSet.csv")
    # Prev results:
    # RF Accuracy: 0.9
    # KNN Accuracy: 0.85
    # DT Accuracy: 0.65
    # SGDC Accuracy: 0.9
    # SVM Accuracy: 0.95

    # Going with KNN for binary Classifcation with average score of 0.85
