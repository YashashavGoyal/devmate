# mate init

The `init` command ensures your local machine is ready for development using DevMate. It acts as a "Doctor" check for your dev environment.

## Detailed Description
`mate init` audits your system for three critical dependencies:
- **Git**: Required for `clone` and `deploy`.
- **Docker**: Required for all container management.
- **Python**: Required for internal CLI logic.

If any tool is missing, DevMate doesn't just error out—it provides official download links and installation guidance tailored to your needs.

## Usage
`mate init [OPTIONS]`

## Options
| Flag | Description |
|------|-------------|
| `-v`, `--verbose` | Show detailed paths and versions of detected tools. |

## Examples

### 1. Standard Environment Check
The first command any new DevMate user should run.
```bash
mate init
```

### 2. Verbose Audit
Useful if you have multiple versions of tools and need to know which one `mate` found.
```bash
mate init --verbose
```

### 3. Alias Support
You can also run this using the `doctor` alias for a friendlier feel.
```bash
mate doctor
```
