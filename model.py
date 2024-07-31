import torch.nn as nn

# SPADModel class which inherits from nn.Module, the base class for all PyTorch modules.
# This class encapsulates the architecture of the neural network.
class SPADModel(nn.Module): 
    def __init__(self): # Constructor
        super(SPADModel, self).__init__()
        # Define network layers
        self.fc1 = nn.Linear(8, 64)  # First layer fully connected (8 inputs: 4 layers 
        # with two parameters: thickness and doping concnetrations, 64 outputs)
        self.fc2 = nn.Linear(64, 64) # Second layer fully connected (64 inputs, 64 outputs)
        self.fc3_PDE = nn.Linear(64, 1) # Output layer for PDE (64 inputs, 1 output)
        self.fc3_DCR = nn.Linear(64, 1) # Output layer for DCR (64 inputs, 1 output)

    def forward(self, x):
        # Pass input data through layers
        x = torch.relu(self.fc1(x)) # Apply the ReLU activation function after the first layer
        x = torch.relu(self.fc2(x)) # Apply the ReLU activation function after the second layer
        PDE = self.fc3_PDE(x) # Calculate PDE output
        DCR = self.fc3_DCR(x) # Calculate DCR output
        return PDE, DCR

# Train
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