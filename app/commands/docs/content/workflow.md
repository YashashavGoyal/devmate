# How to use DevMate

DevMate is designed to take you from a fresh machine to a running app in minutes.

## Scenario A: First Time Setup
1. **Initialize**: Make sure you have the basics.
   ```bash
   mate init
   ```
2. **Start Fast**: Deploy a repository you found.
   ```bash
   mate deploy https://github.com/example/cool-app.git
   ```
3. **Check Status**: Verify everything is running.
   ```bash
   mate status
   ```

## Scenario B: Daily Development
1. **Pull & Up**: Move into your project and start it.
   ```bash
   cd cool-app
   mate up
   ```
2. **Debug**: Check the logs if something is wrong.
   ```bash
   mate logs -f
   ```
3. **Access**: Jump into the container to run a command.
   ```bash
   mate shell
   ```
4. **Shutdown**: When you're done for the day.
   ```bash
   mate down
   ```

## Scenario C: Existing Project
If you already have a project with a `docker-compose.yml` or `Dockerfile`:
1. Run `mate up` in the project root.
2. DevMate will auto-detect your configuration and handle the rest!
