# 🚀 DevMate (mate)

[![Latest Release](https://img.shields.io/github/v/release/YashashavGoyal/devmate?color=blue&label=Download&logo=github&style=for-the-badge)](https://github.com/YashashavGoyal/devmate/releases)

> **Tired of wrestling with cryptic Docker commands and messy container logs?**  
> Stop digging through `docker ps` and meet **DevMate**—the CLI superpower that turns your local development into a clean, automated, and high-speed experience.

**Your friendly local development companion.**

`DevMate` (invoked as `mate`) is a powerful, developer-first CLI tool designed to simplify and orchestrate your local development environments. It provides a clean abstraction layer over Docker and Docker Compose, offering beautiful status reports, automated health checks, and streamlined container management.

---

## ⚡ Quick Download

Prefer a pre-built binary? Grab the latest version for your OS directly from our releases!

[**Download Latest Release**](https://github.com/YashashavGoyal/devmate/releases)

---

## ✨ Key Features

- **🛡️ Smart Health Checks**: Automatically performs TCP and HTTP health checks for your local services.
- **📊 Beautiful Status Table**: Get a clean, Rich-powered overview of all your running containers.
- **🐳 Multi-Config Support**: Works seamlessly with both `docker-compose.yaml` and standalone `Dockerfile` setups.
- **🔄 Git Integration**: Effortlessly clone and deploy repositories to your local environment in one go.
- **🛠️ Developer-Centric**: Built by developers, for developers, with a focus on speed and clarity.

> **IMPORTANT**
> 
> **DevMate** is specifically designed as a **local development companion**. It is **not intended for production usage**.
> 
> For production environments, please use industry-standard orchestrators like Kubernetes, Docker Swarm, or managed cloud services.

## 💻 Installation (From Source)

Since `DevMate` is not yet published to PyPI, you can install it locally for development:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YashashavGoyal/devmate.git
   cd devmate
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies and the package in editable mode**:
   ```bash
   pip install -e .
   ```

Now you can use the `mate` command globally in your terminal!

---

## 🚀 Quick Start

Initialize your environment and check if you have the essential tools:
```bash
mate init
```

Start your services (from a directory with a `compose.yaml` or `Dockerfile`):
```bash
mate up
```

Check the status of your containers:
```bash
mate status
```

---

## 🛠️ Command Reference

| Command | Alias | Description |
| :--- | :--- | :--- |
| `init` | `doctor` | Checks if essential tools (Docker, Git) are installed. |
| `up` | `run` | Starts services and performs health checks. |
| `down` | `stop` | Stops and removes containers. |
| `status` | `ps`, `info`| Displays a beautiful table of running containers. |
| `health` | - | Verifies if the local application is responding. |
| `clone` | - | Clones a git repository to your local system. |
| `deploy` | `dep` | Clones a repository and starts it immediately. |
| `logs` | `log` | Tails the logs of your application services. |
| `shell` | `sh` | Opens an interactive shell inside a container. |
| `version` | - | Shows the current version of `mate`. |
| `about` | - | Displays information about the project. |

---

## 📂 Project Structure

```text
devmate/
├── app/                # Core application logic
│   ├── commands/       # CLI command implementations
│   ├── services/       # Business logic (Docker, Git, Health)
│   └── utils/          # Formatting and display utilities
├── pyproject.toml      # Project metadata and dependencies
└── requirements.txt    # Dependency list
```

---

## 🤝 Contributing

We welcome contributions! Please feel free to open issues or submit pull requests to improve `devmate`.

---

**Author**: Yashashav Goyal

<a href="https://github.com/YashashavGoyal">
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</a>
<a href="https://linkedin.com/in/yashashavgoyal">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
<a href="https://twitter.com/YashashavGoyal">
  <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter" />
</a>

