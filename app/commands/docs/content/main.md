# DevMate (`mate`) — The Developer's Companion

Welcome to the official documentation for **DevMate**. 

DevMate is a high-performance, developer-centric orchestration tool designed to bridge the gap between your local source code and a fully functional containerized environment.

---

## 🛠️ Commands & Examples

Use `mate docs <command>` for even more specialized guides.

### 1. `init` (System Audit)
Ensure your environment is ready.
- **Example**: `mate init`
- **Verbose**: `mate init --verbose`
- **Alias**: `mate doctor`

### 2. `clone` (Smart Fetch)
Download repositories with automatic naming.
- **Default**: `mate clone https://github.com/user/my-app.git`
- **Custom Dir**: `mate clone <URL> --dir ./src`
- **SSH**: `mate clone git@github.com:user/repo.git`

### 3. `up` (Orchestrate)
Build and start your services.
- **Compose**: `mate up` (auto-detects `compose.yaml`)
- **Dockerfile**: `mate up --port 8080:80` (auto-maps local port)
- **Force**: `mate up --force --pull always` (fresh build)

### 4. `deploy` (One-Touch)
Clone and start in one command.
- **Compose Stack**: `mate deploy https://github.com/user/api-stack.git`
- **Single Service**: `mate deploy <URL> --port 3000:3000`
- **Branch/Sub-location**: `mate deploy <URL> --branch dev --location ./app`

### 5. `status` (Monitor)
Real-time dashboard of your containers.
- **Standard**: `mate status`
- **Inspection**: `mate status --volume --health`
- **Filtered**: `mate status --stopped --all`

### 6. `shell` (Interact)
Instant terminal access into containers.
- **Interactive**: `mate shell` (picks best container)
- **Direct**: `mate shell --name redis-service`
- **Custom Shell**: `mate shell --sh /bin/bash`

### 7. `logs` (Stream)
Monitor application output.
- **Follow All**: `mate logs -f`
- **Service Specific**: `mate logs --container api-gw --tail 200`
- **Quick Check**: `mate logs`

### 8. `health` (Audit)
Validate endpoint responsiveness.
- **Local HTTP**: `mate health --port 8080`
- **Internal API**: `mate health -P 5000 -p /health --max-retries 5`
- **TCP Check**: `mate health --url tcp://localhost:5432`

### 9. `down` (Cleanup)
Safe environment shutdown.
- **Compose Reset**: `mate down`
- **Full Removal**: `mate down -v -i` (deletes volumes/images)
- **Specific Container**: `mate down --container-name test-db`

---

## Quick Start - The most common workflow
```bash
mate init                                           # 1. Check system
mate deploy https://github.com/user/project        # 2. Get it running
mate status                                         # 3. Verify services
```
for more workflows run `mate docs workflow`
*DevMate — Build faster, debug less.*
