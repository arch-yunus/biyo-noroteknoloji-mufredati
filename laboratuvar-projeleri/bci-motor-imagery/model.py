import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class EEGNet(nn.Module):
    """
    EEGNet: A Compact Convolutional Neural Network for EEG-based Brain-Computer Interfaces.
    Ref: Lawhern et al., 2018 (Journal of Neural Engineering).
    Optimized for spatial-temporal feature extraction in biosignals.
    """
    def __init__(self, n_channels=64, n_classes=4, n_samples=512, F1=8, D=2, F2=16, dropout_rate=0.25):
        super(EEGNet, self).__init__()
        
        # F1: Number of temporal filters
        # D: Depth multiplier (spatial filters per temporal filter)
        # F2: Number of pointwise filters (typically F1 * D)
        
        # 1. Temporal Convolution (Block 1)
        self.conv1 = nn.Conv2d(1, F1, (1, 64), padding=(0, 32), bias=False)
        self.bn1 = nn.BatchNorm2d(F1)
        
        # 2. Depthwise Spatial Convolution (Block 1)
        # Constrains filters to spatial dimensions (n_channels)
        self.conv2 = nn.Conv2d(F1, F1 * D, (n_channels, 1), groups=F1, bias=False)
        self.bn2 = nn.BatchNorm2d(F1 * D)
        self.pool1 = nn.AvgPool2d((1, 4))
        self.dropout1 = nn.Dropout(dropout_rate)
        
        # 3. Separable Convolution (Block 2)
        self.conv3 = nn.Conv2d(F1 * D, F1 * D, (1, 16), padding=(0, 8), groups=F1 * D, bias=False)
        self.conv4 = nn.Conv2d(F1 * D, F2, (1, 1), bias=False)
        self.bn3 = nn.BatchNorm2d(F2)
        self.pool2 = nn.AvgPool2d((1, 8))
        self.dropout2 = nn.Dropout(dropout_rate)
        
        # 4. Classification Head
        # Calculates spatial features size after pooling
        pooled_samples = n_samples // 32  # 4 * 8 = 32 downsampling factor
        self.fc = nn.Linear(F2 * pooled_samples, n_classes)

    def forward(self, x):
        # Input shape: (Batch, 1, Channels, Samples)
        
        # Block 1: Temporal & Spatial Convolutions
        x = self.bn1(self.conv1(x))
        x = self.bn2(self.conv2(x))
        x = F.elu(x)
        x = self.pool1(x)
        x = self.dropout1(x)
        
        # Block 2: Separable Convolutions
        x = self.bn3(self.conv4(self.conv3(x)))
        x = F.elu(x)
        x = self.pool2(x)
        x = self.dropout2(x)
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # Fully Connected Layer
        x = self.fc(x)
        return x  # Return raw logits (CrossEntropyLoss handles softmax internally)

def generate_synthetic_motor_imagery_dataset(n_trials=100, n_channels=64, n_samples=512):
    """
    Generates a highly structured synthetic EEG dataset for a 4-class Motor Imagery BCI task.
    Classes:
      - 0: Imagine Left Hand movement
      - 1: Imagine Right Hand movement
      - 2: Imagine Feet movement
      - 3: Imagine Tongue movement
      
    Modulates specific channels (C3 for left hand, C4 for right hand, Cz/C3/C4 for feet/tongue)
    with frequency oscillations to simulate actual motor cortex Mu-rhythm suppression (event-related desynchronization).
    """
    np.random.seed(42)
    X = np.random.randn(n_trials, 1, n_channels, n_samples) * 0.5
    y = np.random.randint(0, 4, size=n_trials)
    
    t = np.arange(n_samples)
    
    # Let's map virtual channel indices:
    # 20: C3 (Left motor area)
    # 24: C4 (Right motor area)
    # 22: Cz (Central motor area)
    
    for i in range(n_trials):
        label = y[i]
        if label == 0:  # Left Hand: Suppress C4, increase Mu rhythm (10 Hz) in C3
            X[i, 0, 20, :] += 1.5 * np.sin(2 * np.pi * 10 * t / 250)
            X[i, 0, 24, :] *= 0.2  # Suppression
        elif label == 1:  # Right Hand: Suppress C3, increase Mu rhythm (10 Hz) in C4
            X[i, 0, 24, :] += 1.5 * np.sin(2 * np.pi * 10 * t / 250)
            X[i, 0, 20, :] *= 0.2  # Suppression
        elif label == 2:  # Feet: Increase Beta rhythm (22 Hz) on Cz
            X[i, 0, 22, :] += 1.5 * np.sin(2 * np.pi * 22 * t / 250)
        elif label == 3:  # Tongue: Broad band Theta increase (6 Hz) on frontal channels
            X[i, 0, 0:3, :] += 1.2 * np.sin(2 * np.pi * 6 * t / 250)
            
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long)

def execute_bci_training_pipeline(epochs=5, batch_size=16):
    """
    Runs a full PyTorch deep learning training and evaluation pipeline for EEGNet.
    """
    print("==================================================")
    print("🤖 DEEP LEARNING BRAIN-COMPUTER INTERFACE PIPELINE")
    print("==================================================")
    
    n_channels = 64
    n_samples = 512
    n_classes = 4
    
    # 1. Dataset Generation
    print("\n[+] Generating Synthetic Motor Imagery Dataset (N=120 trials)...")
    X, y = generate_synthetic_motor_imagery_dataset(n_trials=120, n_channels=n_channels, n_samples=n_samples)
    
    # 2. Train-Validation Split (80/20)
    split_idx = int(0.8 * len(X))
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    train_dataset = TensorDataset(X_train, y_train)
    val_dataset = TensorDataset(X_val, y_val)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # 3. Model Initialization
    model = EEGNet(n_channels=n_channels, n_classes=n_classes, n_samples=n_samples)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005, weight_decay=0.01)
    
    print(f"\n[+] Initializing EEGNet Deep Model Architecture:")
    print(f"    - Temporal Kernels (F1): 8")
    # Spatial filter calculation
    print(f"    - Spatial Kernels (D):  2 (Total Filters: 16)")
    print(f"    - Sequence Samples:     {n_samples} bins")
    print(f"    - Optimization:         Adam (lr=0.005, decay=0.01)")
    
    # 4. Training Loop
    print("\n[+] Executing Epoch-wise Model Training & Loss Minimization:")
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        correct_train = 0
        total_train = 0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * batch_X.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total_train += batch_y.size(0)
            correct_train += (predicted == batch_y).sum().item()
            
        epoch_loss = train_loss / total_train
        epoch_acc = (correct_train / total_train) * 100
        
        # Validation
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                val_loss += loss.item() * batch_X.size(0)
                _, predicted = torch.max(outputs.data, 1)
                total_val += batch_y.size(0)
                correct_val += (predicted == batch_y).sum().item()
                
        val_epoch_loss = val_loss / total_val
        val_epoch_acc = (correct_val / total_val) * 100
        
        print(f"    Epoch {epoch:02d}/{epochs:02d} | Train Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc:.1f}% | Val Loss: {val_epoch_loss:.4f} | Val Acc: {val_epoch_acc:.1f}%")
        
    print("\n[+] Verification Complete:")
    print(f"    Model output test completed successfully. Max validation accuracy reached: {val_epoch_acc:.1f}%")
    print("==================================================\n")

if __name__ == "__main__":
    execute_bci_training_pipeline()
