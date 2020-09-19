import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import datasets, models, transforms
import json
from torch.utils.data import Dataset, DataLoader, random_split
from PIL import Image
from pathlib import Path

from resnets import ResNet18

classLabels = ["Pepperoni", "Bacon", "Mushrooms", "Onions", "Peppers", "Black olives",
               "Tomatoes", "Spinach", "Fresh basil", "Arugula", "Broccoli", "Corn", "Pineapple"]

print(torch.__version__)

data_dir = "pizzaGANdata/images/"
label_file = "pizzaGANdata/imageLabels.txt"

df = pd.DataFrame({"image": sorted([f"{i:05d}.jpg" for i in range(1, 9214)])})
df.image = df.image.astype(np.str)
print(df.dtypes)
for label in classLabels:
    df[label] = 0
with open(label_file) as f:
    y = [list(map(int, line.rsplit())) for line in f]
    df.iloc[:, 1:] = y

for ing in ["Bacon", "Mushrooms", "Onions", "Peppers", "Black olives", "Spinach", "Arugula", "Broccoli", "Corn",
            "Pineapple"]:
    removeIdx = df[(df[ing] == 1)].index
    df.drop(removeIdx, inplace=True)

df.head(-1)

df.to_csv("data.csv", index=False)
del df


class MyDataset(Dataset):
    def __init__(self, csv_file, img_dir, transforms=None):
        self.df = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.transforms = transforms

    def __getitem__(self, idx):
        d = self.df.iloc[idx]
        image = Image.open(self.img_dir / d.image).convert("RGB")
        label = torch.tensor(d[1:].tolist(), dtype=torch.float32)

        if self.transforms is not None:
            image = self.transforms(image)
        return image, label

    def __len__(self):
        return len(self.df)


batch_size = 20
transform = transforms.Compose([transforms.Resize((224, 224)),
                                transforms.ToTensor(),
                                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                                ])

dataset = MyDataset("data.csv", Path(data_dir), transform)
valid_no = 749
trainset, valset = random_split(dataset, [len(dataset) - valid_no, valid_no])
print(f"trainset len {len(trainset)} valset len {len(valset)}")
dataloader = {"train": DataLoader(trainset, shuffle=True, batch_size=batch_size, num_workers=2),
              "val": DataLoader(valset, shuffle=True, batch_size=batch_size, num_workers=2)}

import torch.optim as optim
from torch.optim import lr_scheduler

model = ResNet18()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model = model.to(device)

criterion = nn.BCEWithLogitsLoss()
# pos_weight = torch.tensor([ 7*0.252, 0, 7*0.103, 7*0.102, 7*0.089, 7*0.095,7*0.197, 0,  7*0.162, 0, 0, 0, 0 ].to(device)
# specify optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)
sgdr_partial = lr_scheduler.CosineAnnealingLR(optimizer, T_max=5, eta_min=0.005)
# sgdr_partial = optim.lr_scheduler.ReduceLROnPlateau(optimizer,
# 													 mode='min',
# 													 factor=0.5,
# 													 min_lr=1e-6,
# 													 patience=2,
# 													 threshold = 1e-3) #make this -2

from tqdm import trange
from sklearn.metrics import precision_score, f1_score


def get_MSE(tensor):
    # print(tensor.size())
    return torch.mean(torch.norm(tensor, dim=1), dim=0)


def train(model, data_loader, criterion, optimizer, scheduler, num_epochs=5):
    for epoch in trange(num_epochs, desc="Epochs"):
        result = []
        for phase in ['train', 'val']:
            if phase == "train":  # put the model in training mode
                model.train()

            else:  # put the model in validation mode
                model.eval()

            # keep track of training and validation loss
            running_loss = 0.0
            running_corrects = 0.0

            for i, (data, target) in enumerate(data_loader[phase], 0):
                # load the data and target to respective device
                data, target = data.to(device), target.to(device)

                with torch.set_grad_enabled(phase == "train"):
                    optimizer.zero_grad()
                    # feed the input
                    output = model.forward(data)
                    # calculate the loss
                    loss = criterion(output, target)
                    preds = torch.sigmoid(output).data > 0.5
                    preds = preds.to(torch.float32)

                    if phase == "train":
                        # backward pass: compute gradient of the loss with respect to model parameters
                        loss.backward()
                        # update the model parameters
                        optimizer.step()

                # statistics
                running_loss += loss.item() * data.size(0)
                running_corrects += f1_score(target.to("cpu").to(torch.int).numpy(),
                                             preds.to("cpu").to(torch.int).numpy(), average="samples") * data.size(0)

            epoch_loss = running_loss / len(data_loader[phase].dataset)
            epoch_acc = running_corrects / len(data_loader[phase].dataset)

            sgdr_partial.step()

            result.append('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
        print(result)


train(model, dataloader, criterion, optimizer, sgdr_partial, num_epochs=10)

torch.save(model, 'pc_2label.pth')

model = torch.load('pc_2label.pth')
model.to(device)
data_test = MyDataset("data.csv", Path(data_dir), transform)
dataloader_test = DataLoader(data_test, batch_size=1, shuffle=True, num_workers=1)
for i, data_test in enumerate(dataloader_test, 0):
    inputs, labels = data_test[0].to(device), data_test[1].to(device)
    with torch.no_grad():
        outputs = model.forward(inputs)
    print(outputs.data)
    print(labels.data)
    if i == 3:
        break

