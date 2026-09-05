# Windows setup

## Prerequisites

- The repository has already been cloned.
- Python 3.11 or newer is available through the Windows Python launcher.
- GitHub CLI is installed.
- OpenCode is installed and connected to a model provider.
- A fine-grained PAT exists for this repository with only:
  - Contents: read and write
  - Issues: read and write
  - Metadata: read

## 1. Build the isolated Python environment

From the repository root in Command Prompt:

```bat
scripts\bootstrap.cmd
```

Activation is optional. All repository instructions use the venv interpreter explicitly.

## 2. Load the restricted GitHub credential

```bat
scripts\agent-env.cmd
```

`agent-env.cmd` invokes a single built-in PowerShell command only to mask the PAT while you type it; it does not run a `.ps1` script. GitHub CLI, OpenCode, setup, and validation all remain in Command Prompt.

Do not place the token in `.env`, OpenCode configuration, a script, or Git.

Verify the intended identity and repository without displaying the token:

```bat
gh auth status
gh repo view --json nameWithOwner,url,defaultBranchRef
gh auth setup-git
git ls-remote origin
```

## 3. Validate the repository baseline

```bat
scripts\check.cmd
```

## 4. Start OpenCode

```bat
opencode
```

Create a plan from a user-supplied goal:

```text
/plan-project <project goal>
```

Review the generated local planning artifacts, then explicitly authorize publication:

```text
/publish-plan
```

Start a fresh OpenCode session for each unit of work and run:

```text
/execute-next-issue
```

Inspect progress without changing it:

```text
/project-status
```

## 5. End the session

Exit OpenCode and clear the credential from Command Prompt:

```bat
set "GH_TOKEN="
set "PIP_REQUIRE_VIRTUALENV="
```

Revoke the temporary PAT after the demonstration.
