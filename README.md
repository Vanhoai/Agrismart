# 🌾 Agrismart - Smart Farming Assistant

<div align="center">

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1+-00a393.svg)
![YOLO](https://img.shields.io/badge/YOLO-v11-ff6b6b.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

*A Smart Farming Assistant for Sustainable Agriculture and Food Security* 🚀

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[API Documentation](#-api-documentation) •
[Contributing](#-contributing)

</div>

---

## 🎯 About

**Agrismart** is an intelligent farming assistant that leverages computer vision and machine learning to help farmers identify rice leaf diseases, manage agricultural data, and make informed decisions for sustainable agriculture. The system uses advanced YOLO models for real-time disease detection and provides comprehensive tools for farm management.

## ✨ Features

### 🔍 Disease Detection
- **Real-time Rice Leaf Disease Detection** using YOLO v11
- **High Accuracy Classification** with confidence scoring
- **Multiple Disease Types** support (excluding healthy leaves)
- **Image Processing Pipeline** with OpenCV integration

### 📱 User Management
- **OAuth Authentication** with Google Sign-in
- **JWT Token Management** with access/refresh tokens
- **Role-based Access Control** for different user types
- **Device Token Management** for push notifications

### 📊 Data Management
- **Post Creation & Management** with image uploads
- **Submission Tracking** for disease detection results
- **Statistical Analytics** for farm data insights
- **Dataset Management** tools for model training

### 🤖 Machine Learning
- **Custom Dataset Processing** with remake functionality
- **YOLO Model Training** pipeline
- **Computer Vision Utilities** for image processing
- **Model Performance Tracking** and optimization

## 🏗️ Architecture

The project follows a clean architecture pattern with the following structure:

```
📦 Agrismart
├── 🎯 src/                     # Main application source
│   ├── agrismart/              # FastAPI application
│   ├── dataset/                # Dataset management tools
│   ├── training/               # ML model training
│   └── benchmark/              # Performance testing
├── 📦 packages/                # Modular packages
│   ├── core/                   # Core utilities & helpers
│   ├── domain/                 # Business logic & entities
│   ├── infrastructure/         # External services & data
│   └── vision/                 # Computer vision & ML
├── 📊 datasets/               # Training & validation data
├── 📚 docs/                   # Documentation
├── 📓 notebooks/              # Jupyter notebooks
└── 🔧 Configuration files
```

## 🚀 Installation

### Prerequisites

- **Python 3.12+** 🐍
- **Docker & Docker Compose** 🐳
- **MongoDB** 🍃
- **UV Package Manager** ⚡

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/agrismart.git
cd agrismart
```

2. **Install dependencies**
```bash
make sync
```

3. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Download datasets**
```bash
make download
```

5. **Remake dataset for training**
```bash
make remake
```

6. **Start the application**
```bash
docker-compose up -d
```

## 📖 Usage

### 🔧 Dataset Management

**Download Rice Leaf Disease Dataset:**
```bash
uv run dataset --executor download
```

**Generate Dataset Statistics:**
```bash
uv run dataset --executor statistics --dataset all --modes "train valid test"
```

**Remake Dataset for Training:**
```bash
uv run dataset --executor remake
```

### 🎯 Model Training

**Train YOLO Model:**
```bash
uv run training
```

**Run Benchmarks:**
```bash
uv run benchmark
```

### 🌐 API Server

**Start FastAPI Server:**
```bash
uv run agrismart
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### 🔐 Authentication Endpoints

#### OAuth Login
```http
POST /api/v1/auth/oauth
Content-Type: application/json

{
  "idToken": "google_id_token",
  "rawNonce": "nonce_string",
  "deviceToken": "device_token"
}
```

### 📝 Posts Management

#### Create Post
```http
POST /api/v1/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Disease Detection Result",
  "imageUrl": "https://example.com/image.jpg",
  "tags": ["crop", "disease", "rice"],
  "captions": ["Rice leaf with bacterial blight detected"]
}
```

### 🔬 Disease Detection

The system processes images through the vision pipeline:

1. **Image Upload** → Cloud storage (Cloudinary)
2. **Disease Detection** → YOLO model inference  
3. **Result Storage** → MongoDB with confidence scores
4. **Notification** → Firebase push notifications

## 🛠️ Development

### 📁 Project Structure

#### Core Packages

- **[`core`](packages/core/)** - Shared utilities, helpers, and configurations
- **[`domain`](packages/domain/)** - Business entities, use cases, and repository interfaces
- **[`infrastructure`](packages/infrastructure/)** - External service implementations
- **[`vision`](packages/vision/)** - Computer vision and ML components

#### Key Components

- **[`AgrismartBaseDataset`](packages/vision/src/vision/dataset/base_dataset.py)** - Base dataset management
- **[`AgrismartRemakeDataset`](packages/vision/src/vision/dataset/remake_dataset.py)** - Dataset preprocessing
- **[`PostService`](packages/domain/src/domain/services/post_service.py)** - Post management service
- **[`AuthService`](packages/domain/src/domain/services/auth_service.py)** - Authentication service

### 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

### 📊 Dataset Information

The system works with rice leaf disease datasets containing:

- **Bacterial Blight** 🦠
- **Brown Spot** 🟤  
- **Leaf Smut** 🖤
- **Healthy Leaves** (filtered out in remake process) ✅

Dataset format: **YOLO** with bounding box annotations

## 🔧 Configuration

### Environment Variables

```bash
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=agrismart

# Authentication
JWT_SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id

# Cloud Services
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Firebase
FIREBASE_CREDENTIALS_PATH=path/to/credentials.json
```

### 🐳 Docker Configuration

The project includes Docker configuration for easy deployment:

- **FastAPI Application** - Main web service
- **MongoDB** - Database service  
- **Redis** - Caching and task queue
- **Celery** - Background task processing

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository** 🍴
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request** 🚀

### 📋 Development Guidelines

- Follow **PEP 8** style guidelines
- Add **type hints** for all functions
- Write **comprehensive tests**
- Update **documentation** for new features
- Use **conventional commits** format

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Roboflow** for the Rice Leaf Disease dataset
- **Ultralytics** for YOLO implementation
- **FastAPI** for the excellent web framework
- **OpenCV** for computer vision capabilities

## 📞 Contact

**Hinsun** - vanhoai.adv@gmail.com

Project Link: [https://github.com/yourusername/agrismart](https://github.com/yourusername/agrismart)

---

<div align="center">

**Made with ❤️ for sustainable agriculture** 🌱

*Empowering farmers with AI-driven insights* 🚜

</div>