import torch.nn as nn
import torch.optim as optim
import torch
from tqdm import tqdm


class NNClassifier:

    def __init__(self, input_size, hidden_size, output_size):
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters())
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    def fit(self, X, y, epochs, lr, X_val=None, y_val=None):
        if X_val is not None and y_val is not None:
            early_stopping = EarlyStopping(patience=5, min_delta=0)
            X_val = torch.from_numpy(X_val).float().to(self.device)
            y_val = torch.from_numpy(y_val).long().to(self.device)
            val_loss_history = []
        X = torch.from_numpy(X).float().to(self.device)
        y = torch.from_numpy(y).long().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

        train_loss_history = []
        tqdm_epochs = tqdm(range(epochs))
        for epoch in tqdm_epochs:
            running_loss = 0.0
            for x_sample, y_sample in zip(X, y):
                self.optimizer.zero_grad()
                y_pred = self.model(x_sample)
                loss = self.criterion(y_pred, y_sample)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
            avg_train_loss = running_loss / len(X)
            train_loss_history.append(avg_train_loss)
            tqdm_epochs.set_description(f'Epoch {epoch + 1}/{epochs}, Avg Train Loss: {avg_train_loss}')

            if X_val is not None and y_val is not None:
                val_loss = 0.0
                with torch.no_grad():
                    for x_sample, y_sample in zip(X, y):
                        y_pred = self.model(x_sample)
                        loss = self.criterion(y_pred, y_sample)
                        val_loss += loss.item()
                avg_val_loss = val_loss / len(X)
                val_loss_history.append(avg_val_loss)
                early_stopping(avg_val_loss)
                if early_stopping.early_stop:
                    print(f'Early stopping at epoch {epoch + 1}')
                    break
        return train_loss_history, val_loss_history if X_val is not None and y_val is not None else train_loss_history



    def predict(self, x):
        x = torch.from_numpy(x).float().to(self.device)
        logits = self.model(x)
        probabilities = torch.softmax(logits, dim=1)
        predictions = torch.argmax(probabilities, dim=1)
        return predictions, probabilities
    

class EarlyStopping:

    def __init__(self, patience=5, min_delta=0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True