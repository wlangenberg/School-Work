# Import packages
import pandas as pd
import numpy as np
import torch
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader

# We start by reading the data
df = pd.read_csv('../Data/data.txt', names = ['x','y'])

# Plotting the data
df.plot(x='x', y='y', title="Plotting y to x")
plt.show()

# Splitting data into 90/10 train/test datasets.
x_train, x_test, y_train, y_test = train_test_split(df.x, df.y, test_size=0.10, random_state=99)
df_train, df_test = train_test_split(df, test_size=0.20, random_state=99)

# Reshapes data from list of elements to list of lists, i.e. from (160) to (160,1).
reshaper = lambda x: [[element] for element in x ]
# Unshapes the data. Needed to be able to plot the data later.
unshaper = lambda x: [ elements[0] for elements in x ]

# Reshape and cast data to float tensor, needed for pytorch functions.
X_train = torch.FloatTensor(reshaper(x_train.values))
X_test = torch.FloatTensor(reshaper(x_test.values))
Y_train = torch.FloatTensor(reshaper(y_train.values))
Y_test = torch.FloatTensor(reshaper(y_test.values))


# Create a dataset object in a certain format for the dataloader to work.
class dds(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __getitem__(self, index):
        return self.x[index], self.y[index]
    
    def __len__(self):
        return len(self.x)


# Init Dataset object that we created, and also a dataloader that split our data into batches. 
# I set batch_size = 1 to only train the network for one observation at a time.
datasetObject = dds(X_train, Y_train)
train_loader = DataLoader(dataset = datasetObject, batch_size = 1)

# Creating the feed forward neural network architecture.
class FeedForward(torch.nn.Module):
        # Defining our init function for the feedforward class.
        def __init__(self, n_inputs, n_outputs, hidden_size):
            # Initializing the Feedforward class from pytorch nn module.
            super(FeedForward, self).__init__()
            self.inputs = n_inputs
            self.outputs  = n_outputs
            self.hidden = hidden_size
            
            # Defining the layers
            self.fc1 = torch.nn.Linear(self.inputs, self.hidden)
            self.fc2 = torch.nn.Linear(self.hidden, self.hidden)
            self.fc3 = torch.nn.Linear(self.hidden, self.hidden)
            self.fc4 = torch.nn.Linear(self.hidden, self.outputs)
            
            # Defining the actication functions
            self.relu = torch.nn.ReLU()
            self.sigmoid = torch.nn.Sigmoid()
            
            # Initialize weights
            #self.init_weights()
        
        def init_weights(self):
            torch.nn.init.sparse_(self.fc1.weight, sparsity = 0)
            torch.nn.init.sparse_(self.fc2.weight, sparsity = 0)
            torch.nn.init.sparse_(self.fc3.weight, sparsity = 0)
            torch.nn.init.sparse_(self.fc4.weight, sparsity = 0)
            
        def forward(self, features):
            output = self.fc1(features)
            output = self.relu(output)
            output = self.fc2(output)
            output = self.relu(output)
            output = self.fc3(output)
            output = self.relu(output)
            output = self.fc4(output)
            return output

# Create a network object.
model = FeedForward(n_inputs = X_train.shape[1], n_outputs = 1, hidden_size = 200)

# Create a loss criteria and optimizer.
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr = 0.0001)

# Train the network
epochs = 60
valid_losses = []
train_losses = []

for epoch in range(epochs):
    for features, targets in train_loader:
        # Forward propagation
        output = model.forward(features)
        # Calculate the loss
        loss = criterion(output, targets)
        # Initialize the gradient to zero
        optimizer.zero_grad()
        # Back propagation
        loss.backward()
        # Update the weights
        optimizer.step()
        
    # Stop the training
    model.eval() 
    
    # Save the losses
    train_loss = criterion(model(X_train), Y_train).item()
    valid_loss = criterion(model(X_test), Y_test).item()
    train_losses.append(train_loss)
    valid_losses.append(valid_loss)
    
    print(f"train loss: {train_loss}, val loss: {valid_loss}")
    
    model.train()

# Plot training loss and  validation loss for each epoch
x = range(len(train_losses))

plt.plot(x, train_losses, label = "Train Loss")
plt.plot(x, valid_losses, label = "Validation Loss")
plt.legend()
plt.show()

# Plotting predicted vs actual values using validation data.
Y_test_pred = unshaper(model(X_test).detach().numpy())
results = pd.DataFrame({'x':unshaper(X_test.numpy()), 'y_test':unshaper(Y_test.numpy()), 'y_test_pred':Y_test_pred}).sort_values('x')
training_data = pd.DataFrame({'x':unshaper(X_train.numpy()), 'y_train':unshaper(Y_train.numpy())}).sort_values('x')

plt.plot(range(len(X_test)), results['y_test'], label="Y_test")
plt.plot(range(len(X_test)), results['y_test_pred'],label= "Y_test_pred")
plt.title("Predicted and actual values using validation data")
plt.legend()
plt.show()

# Plotting predicted vs actual values using all data.
Y_pred = model(torch.FloatTensor(torch.FloatTensor(reshaper(df['x'].values))))
Y_pred = unshaper(Y_pred.detach().numpy())
df['y_pred'] = Y_pred
df.plot(x = 'x', title="Predicted and actual values using all data")
plt.plot()
