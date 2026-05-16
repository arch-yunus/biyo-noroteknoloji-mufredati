import torch
import torch.nn as nn
import torch.nn.functional as F

class EEGNet(nn.Module):
    """
    EEGNet architecture for BCI classification.
    Ref: Lawhern et al., 2018.
    """
    def __init__(self, n_channels, n_classes, n_samples):
        super(EEGNet, self).__init__()
        self.T = n_samples
        
        # Temporal Convolution
        self.conv1 = nn.Conv2d(1, 16, (1, 64), padding=(0, 32), bias=False)
        self.batchnorm1 = nn.BatchNorm2d(16)
        
        # Depthwise Convolution
        self.conv2 = nn.Conv2d(16, 32, (n_channels, 1), groups=16, bias=False)
        self.batchnorm2 = nn.BatchNorm2d(32)
        self.pooling1 = nn.AvgPool2d((1, 4))
        
        # Separable Convolution
        self.conv3 = nn.Conv2d(32, 32, (1, 16), padding=(0, 8), groups=32, bias=False)
        self.conv4 = nn.Conv2d(32, 32, (1, 1), bias=False)
        self.batchnorm3 = nn.BatchNorm2d(32)
        self.pooling2 = nn.AvgPool2d((1, 8))
        
        # Fully Connected
        self.fc = nn.Linear(32 * (n_samples // 32), n_classes)

    def forward(self, x):
        # x shape: (Batch, 1, Channels, Samples)
        x = self.batchnorm1(self.conv1(x))
        
        x = self.batchnorm2(self.conv2(x))
        x = F.elu(x)
        x = self.pooling1(x)
        x = F.dropout(x, 0.25)
        
        x = self.batchnorm3(self.conv4(self.conv3(x)))
        x = F.elu(x)
        x = self.pooling2(x)
        x = F.dropout(x, 0.25)
        
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return F.log_softmax(x, dim=1)

if __name__ == "__main__":
    # Mock data: 1 batch, 1 channel (virtual), 64 EEG channels, 500 samples
    n_channels = 64
    n_samples = 512
    model = EEGNet(n_channels=n_channels, n_classes=4, n_samples=n_samples)
    
    mock_input = torch.randn(1, 1, n_channels, n_samples)
    output = model(mock_input)
    
    print(f"Model Architecture:\n{model}")
    print(f"Output shape: {output.shape} (Expected: [1, 4])")
