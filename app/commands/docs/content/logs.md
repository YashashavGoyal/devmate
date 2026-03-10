# mate logs

The `logs` command streams the output of your application to your terminal, making it easy to monitor activity and catch errors as they happen.

## Detailed Description
DevMate `logs` integrates with both Docker Compose and standalone containers. It supports "follow" mode for real-time monitoring and allows you to limit the output history using the "tail" option to avoid terminal clutter.

## Usage
`mate logs [OPTIONS]`

## Options
| Flag | Description |
|------|-------------|
| `-f`, `--follow` | Stream logs in real-time until interrupted (Ctrl+C). |
| `-t`, `--tail` | Number of recent lines to display (default: 100). |
| `-c`, `--container` | Explicitly fetch logs for a specific container name. |
| `-p`, `--path` | Project path for fetching Compose-wide logs. |

## Examples

### 1. Project Monitoring (Compose)
Follows logs from ALL services in your current stack simultaneously.
```bash
mate logs -f
```

### 2. Debugging a Specific Service
Shows the last 500 lines for a specific container.
```bash
mate logs --container web-api --tail 500
```

### 3. Quick Inspection
Checks the recent history of the current folder's project without streaming.
```bash
mate logs
```
