import galai as gal
import torch

model = gal.load_model("mini", num_gpus=torch.cuda.available_devices())
result = model.generate("Literature review on hardware accelerators", tokens=200)

print(result)