# mate shell

The `shell` command provides instant access into any running container, allowing you to run management commands, inspect logs, or debug the environment directly.

## Detailed Description
`mate shell` is your primary tool for "Inside-the-box" debugging. It automatically detects the most relevant container in your current project directory. If your project has multiple containers (Compose), it provides an interactive selection menu.

## Usage
`mate shell [OPTIONS]`

## Options
| Flag | Description |
|------|-------------|
| `-n`, `--name` | Name of the container or Compose service to connect to. |
| `-s`, `--sh` | Shell executable to use (default: `/bin/sh`). |
| `-p`, `--path` | Project directory for auto-detection logic. |

## Examples

### 1. Interactive Selection (Compose)
If you have multiple services, DevMate will let you pick the one you want.
```bash
mate shell
```

### 2. Direct Container Access
Quickly jump into a known container to check a specific file or process.
```bash
mate shell --name my-redis-cache
```

### 3. Custom Shell (Bash)
Use this if the container has `bash` installed for a more feature-rich experience.
```bash
mate shell --sh /bin/bash
```
