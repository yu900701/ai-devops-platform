# =========================
# Step 0 - Windows DevOps Environment
# =========================

# 1. 更新 Windows 與 NVIDIA Driver（手動操作）

# 2. 啟用 Windows 功能（手動操作）
# 勾選：
# - 適用於 Linux 的 Windows 子系統
# - 虛擬機器平台

# 3. BIOS 開啟 SVM Mode（手動操作）
# ASUS TUF Gaming FX505DD 建議：
# UMA Buffer Size -> Auto

# 4. 安裝 WSL2
wsl --install

# 5. 安裝 Ubuntu
wsl --install -d Ubuntu

# 6. 驗證 WSL
wsl -l -v

# =========================
# Step 0-2 Docker Desktop
# =========================

# 安裝 Docker Desktop 時勾選：
# Use WSL2 instead of Hyper-V

# 在 Docker Desktop Settings勾選：
# Enable integration with additional distros: Ubuntu


# Docker Desktop:
# Settings -> Resources -> WSL Integration
# 啟用 Ubuntu

# 驗證 Docker
docker ps

# =========================
# Step 0-3 Ubuntu Package Update
# =========================

sudo apt update

# =========================
# Step 0-4 Install kubectl
# =========================

sudo apt install -y kubectl

# 驗證 kubectl
kubectl version --client

# =========================
# Step 0-5 Install k3d
# =========================

curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# 驗證 k3d
k3d version

# =========================
# Step 0-6 Create Kubernetes Cluster
# =========================

k3d cluster create dev-cluster

# 驗證 Kubernetes
kubectl get nodes

# 驗證 k3d cluster
k3d cluster list

# =========================
# Step 0-7 Install Helm
# =========================

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 驗證 Helm
helm version

# =========================
# Step 0-8 Install Git
# =========================

sudo apt install -y git

# 驗證 Git
git --version