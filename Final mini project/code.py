import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, f1_score, jaccard_score
import itertools

# Function to plot confusion matrix
def plot_confusion_matrix(cm, classes, title='Confusion Matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], '.2f'), horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

class CancerPredictionApp:
    def __init__(self, master):
        self.master = master
        master.title("Cancer Cell Prediction")
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 10, "bold"))
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#333333")

        # Create header frame
        self.header_frame = ttk.Frame(master, padding=(10, 10))
        self.header_frame.pack(fill="x")
        
        self.header_label = ttk.Label(self.header_frame, text="Cancer Cell Prediction using Random Forest and SVM", style="Header.TLabel")
        self.header_label.pack()

        # Create main content frame
        self.content_frame = ttk.Frame(master, padding=(20, 20))
        self.content_frame.pack(fill="both", expand=True)

        # Add buttons and labels
        self.load_button = ttk.Button(self.content_frame, text="Load Dataset", command=self.load_data, style="TButton")
        self.load_button.grid(row=0, column=0, pady=10)

        self.model_var = tk.StringVar(value="Random Forest")
        self.rf_radio = ttk.Radiobutton(self.content_frame, text="Random Forest", variable=self.model_var, value="Random Forest")
        self.svm_radio = ttk.Radiobutton(self.content_frame, text="SVM", variable=self.model_var, value="SVM")
        self.rf_radio.grid(row=1, column=0, pady=10, sticky="w")
        self.svm_radio.grid(row=1, column=1, pady=10, sticky="w")

        self.train_button = ttk.Button(self.content_frame, text="Train Model", command=self.train_model, state=tk.DISABLED, style="TButton")
        self.train_button.grid(row=2, column=0, pady=10)

        self.predict_button = ttk.Button(self.content_frame, text="Predict Cancer", command=self.predict_cancer, state=tk.DISABLED, style="TButton")
        self.predict_button.grid(row=2, column=1, pady=10)

        self.plot_button = ttk.Button(self.content_frame, text="Show Confusion Matrix", command=self.show_confusion_matrix, state=tk.DISABLED, style="TButton")
        self.plot_button.grid(row=3, column=0, pady=10)

        self.result_label = ttk.Label(self.content_frame, text="", style="TLabel", anchor="center")
        self.result_label.grid(row=4, column=0, pady=20, columnspan=2)

        self.data = None
        self.model = None
        self.training_X = None
        self.test_X = None
        self.training_y = None
        self.test_y = None

        # Add entry fields
        tk.Label(self.content_frame, text="Clump Thickness:").grid(row=5, column=0)
        self.entry_clump = tk.Entry(self.content_frame)
        self.entry_clump.grid(row=5, column=1)

        tk.Label(self.content_frame, text="Uniformity of Cell Size:").grid(row=6, column=0)
        self.entry_unif_size = tk.Entry(self.content_frame)
        self.entry_unif_size.grid(row=6, column=1)

        tk.Label(self.content_frame, text="Uniformity of Cell Shape:").grid(row=7, column=0)
        self.entry_unif_shape = tk.Entry(self.content_frame)
        self.entry_unif_shape.grid(row=7, column=1)

        tk.Label(self.content_frame, text="Marginal Adhesion:").grid(row=8, column=0)
        self.entry_marg_adh = tk.Entry(self.content_frame)
        self.entry_marg_adh.grid(row=8, column=1)

        tk.Label(self.content_frame, text="Single Epithelial Cell Size:").grid(row=9, column=0)
        self.entry_sing_epi_size = tk.Entry(self.content_frame)
        self.entry_sing_epi_size.grid(row=9, column=1)

        tk.Label(self.content_frame, text="Bare Nuclei:").grid(row=10, column=0)
        self.entry_bare_nuc = tk.Entry(self.content_frame)
        self.entry_bare_nuc.grid(row=10, column=1)

        tk.Label(self.content_frame, text="Bland Chromatin:").grid(row=11, column=0)
        self.entry_bland_chrom = tk.Entry(self.content_frame)
        self.entry_bland_chrom.grid(row=11, column=1)

        tk.Label(self.content_frame, text="Normal Nucleoli:").grid(row=12, column=0)
        self.entry_norm_nucl = tk.Entry(self.content_frame)
        self.entry_norm_nucl.grid(row=12, column=1)

        tk.Label(self.content_frame, text="Mitoses:").grid(row=13, column=0)
        self.entry_mit = tk.Entry(self.content_frame)
        self.entry_mit.grid(row=13, column=1)

    # Function to load the dataset
    def load_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.data = pd.read_csv(file_path)
            self.data = self.data[pd.to_numeric(self.data['BareNuc'], errors="coerce").notnull()]
            self.data["BareNuc"] = self.data["BareNuc"].astype('int64')
            self.train_button.config(state=tk.NORMAL)
            messagebox.showinfo("Dataset Loaded", "Dataset loaded successfully!")

    # Function to train the model
    def train_model(self):
        if self.data is not None:
            X = np.asanyarray(self.data[['Clump', 'UnifSize', 'UnifShape', 'MargAdh', 
                                         'SingEpiSize', 'BareNuc', 'BlandChrom', 'NormNucl', 'Mit']])
            y = np.asanyarray(self.data['Class'].astype('int'))

            self.training_X, self.test_X, self.training_y, self.test_y = train_test_split(X, y, test_size=0.2, random_state=42)
            selected_model = self.model_var.get()
            if selected_model == "Random Forest":
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                self.model = SVC(kernel='linear')

            self.model.fit(self.training_X, self.training_y)
            self.plot_button.config(state=tk.NORMAL)
            self.predict_button.config(state=tk.NORMAL)
            messagebox.showinfo("Model Trained", f"{selected_model} model trained successfully!")

    # Function to predict cancer
    def predict_cancer(self):
        try:
            input_features = [
                float(self.entry_clump.get()), 
                float(self.entry_unif_size.get()), 
                float(self.entry_unif_shape.get()), 
                float(self.entry_marg_adh.get()), 
                float(self.entry_sing_epi_size.get()), 
                float(self.entry_bare_nuc.get()), 
                float(self.entry_bland_chrom.get()), 
                float(self.entry_norm_nucl.get()), 
                float(self.entry_mit.get())
            ]
            input_data = np.array(input_features).reshape(1, -1)
            prediction = self.model.predict(input_data)
            result = "Benign (2)" if prediction == 2 else "Malignant (4)"
            messagebox.showinfo("Prediction Result", f"The predicted class is: {result}")
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please enter valid numbers for all features.\nError: {ve}")

    # Function to show the confusion matrix
    def show_confusion_matrix(self):
        if self.model is not None:
            y_hat = self.model.predict(self.test_X)
            cf_matrix = confusion_matrix(self.test_y, y_hat, labels=[2, 4])
            plt.figure()
            plot_confusion_matrix(cf_matrix, classes=['Benign (2)', 'Malignant (4)'], title=f'{self.model_var.get()} Confusion Matrix')
            plt.show()

            report = classification_report(self.test_y, y_hat)
            f1 = f1_score(self.test_y, y_hat, average="weighted")
            jaccard = jaccard_score(self.test_y, y_hat, pos_label=2)
            result_text = f"Classification Report:\n{report}\nF1 Score: {f1}\nJaccard Index: {jaccard}"
            self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CancerPredictionApp(root)
    root.mainloop()
