from model import SPADModel
import torch.nn as nn
import torch
import pandas as pd
from sklearn.model_selection import train_test_split

# Prepare data

# Load data: DataFrame df containing the data.
df = pd.read_csv('data.csv')

# Data separation
X = df[['thickness1', 'doping1', 'thickness2', 'doping2', 
        'thickness3', 'doping3', 'thickness4', 'doping4']] # input characteristics matrix.
y_PDE = df['PDE']
y_DCR = df['DCR']

# Divides the data into training sets (80%) and test sets (20%). 
X_train, X_test, y_PDE_train, y_PDE_test, y_DCR_train, y_DCR_test = train_test_split(X, y_PDE, y_DCR, test_size=0.2, random_state=42)

# Conversion to PyTorch tensors
X_train = torch.tensor(X_train.values, dtype=torch.float32)
y_PDE_train = torch.tensor(y_PDE_train.values, dtype=torch.float32).view(-1, 1)
y_DCR_train = torch.tensor(y_DCR_train.values, dtype=torch.float32).view(-1, 1)
X_test = torch.tensor(X_test.values, dtype=torch.float32)
y_PDE_test = torch.tensor(y_PDE_test.values, dtype=torch.float32).view(-1, 1)
y_DCR_test = torch.tensor(y_DCR_test.values, dtype=torch.float32).view(-1, 1)

# Trainning

model = SPADModel()
criterion = nn.MSELoss() # Use the mean square error (MSE) as a loss function
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # Use the Adam optimiser

# Drive loop where we pass the train data through the model, calculate the losses, 
# then update the model weights using the Adam optimizer.
num_epochs = 1000
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad() # Reset gradients
    PDE_pred, DCR_pred = model(X_train)
    loss_PDE = criterion(PDE_pred, y_PDE_train) # Calculate the loss for PDE
    loss_DCR = criterion(DCR_pred, y_DCR_train) # Calculate the loss for DCR
    loss = loss_PDE + loss_DCR
    loss.backward() # Calculate gradients
    optimizer.step() # Update weights
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, PDE Loss: {loss_PDE.item():.4f}, DCR Loss: {loss_DCR.item():.4f}')
