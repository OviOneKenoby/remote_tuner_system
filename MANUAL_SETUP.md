# Exact manual setup and operating steps

## Initialize and publish once

1. Extract the ZIP to a writable folder outside the synced `sources/` directory. Open the extracted `REMOTE-TUNER-SYSTEM` folder. Git and a hosting account are required for publication; install/sign in if needed.
2. Create an **empty private repository** named `REMOTE-TUNER-SYSTEM` on your chosen Git host. Do not pre-create a README/license there. Copy its actual repository URL. No remote repository was created by this package.
3. In a terminal inside the extracted folder run the commands below. Replace `<actual-repository-url>` with the real URL. If Git requests identity, configure your actual name/email, then retry the commit. Authenticate using the host's normal sign-in flow; never put tokens in documentation.

```powershell
git init -b main
git add .
git commit -m "Initialize REMOTE and TUNER coordination"
git remote add origin <actual-repository-url>
git push -u origin main
```

4. Give the PM, REMOTE and TUNER execution environments access to this same repository. For local Codex execution provide a writable coordination checkout path as well as the appropriate firmware checkout. For other machines clone the published repository. Avoid concurrent edits in one checkout; use separate branches/checkouts and merge reviewed changes. Configure host permissions and branch protection if multiple accounts will write.
5. Supply the missing reference artifacts listed in references/README.md or accessible immutable links. Supply actual firmware repository URLs/paths and REMOTE baseline. Record hashes and original approval evidence; do not change the preserved facts just because a historical candidate has an older header.
6. Give the PM the current repository snapshot/access and the content of prompts/PROJECT_MANAGER_BOOTSTRAP.md. Give each specialized chat its device context and current coordination files. Repository URL alone does not guarantee chat access; if an actor cannot read it, upload/paste the needed current files and state the coordination commit.

## Manual cycle until a runner is configured

1. Invoke PM to review current handoffs and publish the next scoped assignments.
2. Invoke REMOTE//01 and/or TUNER//01 with their assignment and current coordination revision. Each produces its Codex prompt.
3. Start Codex with that prompt, real firmware checkout and writable coordination checkout. If it cannot publish, manually commit/push the reviewed handoff branch. Merge reviewed branches, update all readers, and give PM the final coordination commit.
4. Invoke PM again to review the published handoffs and update the plan/gate. Repeat.
5. Provide physical hardware and perform requested device tests when local automation lacks access. Return logs and flashed commit. Approve or reject shared-contract proposals personally with exact scope; no actor can infer your approval.

You do not need to retype handoff contents when actors can read/write the shared repo. You still initiate this cycle and transfer current snapshots to actors without direct access. This starter does not configure autonomous scheduling or chat-to-chat dispatch. To automate later, choose and configure a runner with repository credentials, task routing, scheduling and reviewed publication; that is separate work.
