# mate status

The `status` command provides a real-time, color-coded dashboard of your container environment. It's designed to be much more readable than standard `docker ps` output.

## Detailed Description
DevMate `status` summarizes the state of all containers. It includes health indicators (green dots for healthy, red for down), shortened image names for clarity, and port mapping summaries. It can be customized to show exactly the data you need using the `--format` flag.

## Usage
`mate status [OPTIONS]`

## Options
| Flag | Description |
|------|-------------|
| `-a`, `--all` | Show all containers (including stopped/exited). |
| `--stopped` | Filter view to only stopped containers. |
| `-v`, `--volume` | Include mounted volumes in the table output. |
| `--health` | Show detailed health check results. |
| `--format` | Customize columns: `name,image,status,ports,id,network,mounts`. |

## Examples

### 1. Standard Dashboard (Running Services)
Perfect for checking if your Compose stack is up and healthy.
```bash
mate status
```

### 2. Resource Inspection (Volumes & Mounts)
Useful for debugging persistence issues or checking where data is stored.
```bash
mate status --volume --mounts
```

### 3. Custom Scriptable Format
Outputs only specific columns, useful for piping into other tools.
```bash
mate status --format "name,status,id"
```
