# mate clone

The `clone` command allows you to download a Git repository to your local machine. DevMate handles destination path logic automatically if you don't specify one, following standard naming conventions.

## Detailed Description
`mate clone` uses Git to download the specified repository. If no directory is provided, it extracts the repository name from the URL and creates a folder with that name in the current directory. It is the fundamental first step before running `mate up` or other management commands.

## Usage
`mate clone <URL> [OPTIONS]`

## Arguments & Options
| Flag | Description |
|------|-------------|
| `URL` | The Git URL of the repository (required). |
| `-d`, `--dir` | Custom directory path where the repo will be cloned. |

## Examples

### 1. Default Logic (Automatic Naming)
Clones the repository and names the folder after the repo name (e.g., `my-app`).
```bash
mate clone https://github.com/user/my-app.git
```

### 2. Specific Directory
Clones the repository into a predetermined folder structure.
```bash
mate clone https://github.com/user/my-app.git --dir ./projects/client-a
```

### 3. SSH Support
Works with SSH URLs if your system is configured with Git keys.
```bash
mate clone git@github.com:user/my-app.git
```
