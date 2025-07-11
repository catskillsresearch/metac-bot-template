# How to run LLM server

1. Go to tensordock and spin up the instance
2. Login into the instance using the ssh command "ssh -p yyyyy -L 11434:localhost:11434 user@x.y.z.w".  Check on the tensordock server status plage for the exact IP address needed for the last part.
3. First time, run

```
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```
... logout and login again.

## Add the NVIDIA Container Toolkit repository

```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Test nvidia-smi

```
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
```

### Run server (first time)

```
docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama catskillsresearch/ollama-docker-ollama:latest
```
### Run server (next time)

```
docker start ollama
```

### NVITop

```
sudo apt install -y nvitop
nvitop
```

### Shutdown

```
sudo shutdown now
```

Shut down check on [TensorDock console](https://dashboard.tensordock.com/my-servers).
