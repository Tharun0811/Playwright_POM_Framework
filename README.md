# Jenkins + GitHub Webhook + Cloudflare Tunnel Integration

## 1. Objective

The objective of this setup is to automatically trigger a Jenkins pipeline whenever code is pushed to GitHub.

Without a webhook, Jenkins can periodically check GitHub for changes using polling.

With a webhook, GitHub notifies Jenkins immediately when a push event occurs.

### Overall workflow

```text
Developer
    |
    | Push code
    v
GitHub Repository
    |
    | Push event notification
    v
GitHub Webhook
    |
    v
Cloudflare Tunnel
    |
    | Forwards request to localhost:8080
    v
Local Jenkins Server
    |
    v
Jenkins Pipeline
    |
    | Checkout
    | Setup Python
    | Install dependencies
    | Execute pytest
    | Publish HTML report
    v
Test Results
```

---

## 2. Tools Used

| Tool | Purpose |
|---|---|
| Git | Version control |
| GitHub | Remote repository |
| Jenkins | CI/CD automation |
| GitHub Plugin | Receives GitHub webhook notifications |
| Cloudflare Tunnel | Makes local Jenkins accessible through a public URL |
| Python | Executes automation scripts |
| Playwright | Browser automation |
| Pytest | Test execution |

---

## 3. Step 1: Verify Jenkins

Our Jenkins server runs locally.

Jenkins URL:

```text
http://localhost:8080
```

Port `8080` is the port on which Jenkins is accessible.

### Why do we need Cloudflare Tunnel?

Our Jenkins server is running on our local computer.

GitHub is an external service. It cannot normally access our computer through `localhost`.

For GitHub to send webhook notifications to Jenkins, Jenkins needs an accessible endpoint.

Cloudflare Tunnel provides a temporary public URL that forwards requests to our local Jenkins server.

---

## 4. Step 2: Install Cloudflare Tunnel

We used WinGet to install Cloudflared.

Command:

```powershell
winget install --id Cloudflare.cloudflared
```

Verify installation:

```powershell
cloudflared --version
```

Our installed version:

```text
cloudflared version 2026.10.7
```

If PowerShell does not recognize the command immediately after installation, close and reopen PowerShell so it can refresh the PATH.

---

## 5. Step 3: Start Cloudflare Quick Tunnel

Open a separate PowerShell window.

Execute:

```powershell
cloudflared tunnel --url http://localhost:8080
```

### What does this command mean?

- `cloudflared` starts the Cloudflare Tunnel client.
- `tunnel` tells Cloudflared to create a tunnel.
- `--url` specifies the local service to which requests should be forwarded.
- `http://localhost:8080` is our local Jenkins address.

Cloudflare generates a temporary public URL.

Example from our practice session:

```text
https://camping-prisoners-laid-bend.trycloudflare.com
```

### Important points

1. Keep the PowerShell window running.
2. Closing the window stops the tunnel.
3. The Quick Tunnel URL is temporary.
4. A new tunnel may generate a different URL.
5. GitHub must use the currently active tunnel URL.

### Verify the tunnel

Open the generated HTTPS URL in a browser.

We verified that the Jenkins login page appeared successfully.

We also tested it using an Incognito window.

---

## 6. Step 4: Configure Jenkins GitHub Webhook Trigger

Open Jenkins:

```text
http://localhost:8080
```

Navigate to:

```text
Dashboard
    |
    v
Playwright_Pipeline_CI
    |
    v
Configure
    |
    v
Build Triggers
```

Enable:

```text
GitHub hook trigger for GITScm polling
```

Click Save.

### What does this option do?

It tells Jenkins to respond to GitHub webhook notifications.

When GitHub sends a push notification, Jenkins can initiate SCM polling to check whether the configured source-control branch has changed.

If Jenkins detects relevant changes, the pipeline can start automatically.

---

## 7. Step 5: Configure GitHub Webhook

Open the GitHub repository:

```text
https://github.com/Tharun0811/Playwright_POM_Framework
```

Navigate to:

```text
Repository
    |
    v
Settings
    |
    v
Webhooks
    |
    v
Add webhook
```

### Webhook configuration

**Payload URL**

```text
https://YOUR-CLOUDFLARE-URL/github-webhook/
```

Example from our session:

```text
https://camping-prisoners-laid-bend.trycloudflare.com/github-webhook/
```

**Content type**

```text
application/json
```

**Secret**

We left this empty for our short practice setup because we had not configured a matching secret in Jenkins.

For a real environment, configure webhook secret verification on the Jenkins side and use the same secret in GitHub.

**Which events should trigger this webhook?**

Select:

```text
Just the push event
```

**Active**

Keep it checked.

Finally, click:

```text
Add webhook
```

### What is a push event?

A push event is generated when someone pushes commits to a GitHub repository.

Example:

```text
git add .
git commit -m "Update test cases"
git push origin feature-branch
```

GitHub sends a webhook notification when this push happens.

---

## 8. Step 6: Verify Webhook Connectivity

After creating the webhook:

Navigate to:

```text
GitHub Repository
    |
    v
Settings
    |
    v
Webhooks
    |
    v
Select your webhook
    |
    v
Recent Deliveries
```

GitHub sends an initial `ping` event when the webhook is created.

We received:

```text
HTTP 200
```

### What does HTTP 200 mean?

HTTP 200 means the request was successfully received and handled by the endpoint.

In our case, it confirmed that GitHub could reach the Jenkins webhook endpoint through Cloudflare Tunnel.

Important distinction:

HTTP 200 for the initial ping confirms connectivity. It does not yet prove that an actual Git push triggers the Jenkins pipeline.

We still need to test a real push event.

---

## 9. Step 7: Git Commands for Feature Branch Practice

We decided not to commit directly to `master`.

Instead, we created a separate feature branch.

### Navigate to the project

```powershell
cd C:\Playwright_POM_Framework
```

### Check available branches

```powershell
git branch
```

The `*` symbol identifies the current branch.

### Check working directory status

```powershell
git status
```

Output:

```text
nothing to commit, working tree clean
```

This means there are no uncommitted changes.

### Switch to master

```powershell
git switch master
```

### Get the latest changes from GitHub

```powershell
git pull origin master
```

This updates the local master branch with the latest remote changes.

### Create a new feature branch

```powershell
git switch -c webhook-practice
```

This command creates a new branch and switches to it.

Our actual branch name was:

```text
weebhook-pratice
```

### Verify the current branch

```powershell
git branch
```

### Check status again

```powershell
git status
```

We confirmed that the working tree was clean.

---

## 10. Step 8: Git Commands to Commit and Push

After preparing the README revision notes:

### Check changed files

```powershell
git status
```

### Stage the README file

```powershell
git add README.md
```

Staging means selecting the file that should be included in the next commit.

### Commit the changes

```powershell
git commit -m "Add Jenkins webhook integration notes"
```

A commit saves a snapshot of the staged changes in local Git history.

### Push the feature branch to GitHub

Use the actual branch name:

```powershell
git push -u origin weebhook-pratice
```

`origin` represents the remote GitHub repository.

`-u` sets the upstream tracking relationship between the local branch and the remote branch.

After the first push, subsequent pushes can generally use:

```powershell
git push
```

---

## 11. Important: Jenkins Branch Configuration

Our Jenkins pipeline currently checks out:

```text
*/master
```

This is important.

Even if GitHub successfully sends a webhook notification when we push to a feature branch, Jenkins may not start a build because its SCM configuration is watching `master`.

The webhook notification and Jenkins branch configuration perform different jobs:

- Webhook: Notifies Jenkins that a repository event occurred.
- Branch specification: Determines which branch Jenkins checks out and monitors.

For our feature-branch test, we may need to configure a separate Jenkins job or a suitable multibranch pipeline.

We should not change the existing working pipeline blindly.

---

## 12. Troubleshooting Reference

| Problem | Possible reason |
|---|---|
| `cloudflared` not recognized | PATH not refreshed |
| Cloudflare URL not reachable | Tunnel is stopped |
| GitHub webhook delivery fails | Incorrect URL or Jenkins unreachable |
| HTTP 404 | Incorrect webhook endpoint |
| HTTP 403 | Request rejected by server or security configuration |
| Webhook returns HTTP 200 but no build starts | Jenkins trigger or SCM branch configuration issue |
| Jenkins does not detect feature branch push | Job is configured to monitor master |
| Pipeline fails during execution | Jenkinsfile, Python, dependencies or browser configuration issue |

---

## 13. Security and Cleanup

Cloudflare Quick Tunnel makes our local Jenkins endpoint publicly reachable while the tunnel is running.

For our learning exercise:

1. Keep the tunnel active only while testing.
2. Never share Jenkins admin credentials.
3. Configure webhook secret verification for a more secure setup.
4. Delete the temporary GitHub webhook when finished if it is no longer needed.
5. Stop Cloudflare Tunnel using `Ctrl + C` in its PowerShell window.

Remember: Jenkins login authentication does not automatically mean every endpoint, including the webhook endpoint, has the same authentication requirements.

---

## 14. Interview Revision Questions

1. What is a GitHub webhook?
2. What is the difference between polling and a webhook?
3. Why do we need Cloudflare Tunnel when Jenkins is installed locally?
4. What is the purpose of `/github-webhook/`?
5. Why do we select `application/json`?
6. What is the purpose of the GitHub push event?
7. What does HTTP 200 indicate?
8. What is the purpose of `GitHub hook trigger for GITScm polling`?
9. Why can a feature-branch push fail to trigger a Jenkins job configured for master?
10. What is the difference between a webhook and a Jenkins multibranch pipeline?

---

## 15. Final Revision: Complete Flow

```text
1. Install Cloudflared
        |
2. Start Cloudflare Quick Tunnel
        |
3. Obtain public HTTPS URL
        |
4. Open Jenkins job configuration
        |
5. Enable GitHub hook trigger
        |
6. Configure GitHub webhook
        |
7. Select push event
        |
8. Save webhook
        |
9. Verify HTTP 200 response
        |
10. Create feature branch
        |
11. Make a README change
        |
12. Commit and push feature branch
        |
13. Verify GitHub delivery
        |
14. Verify Jenkins build trigger
```

**Key takeaway:** GitHub Webhooks allow GitHub to notify Jenkins about repository events instead of Jenkins having to repeatedly check GitHub for changes.

Tested 