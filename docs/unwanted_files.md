# Unwanted and Temporary Files List

This document lists files and directories in the JanAI repository that are either one-off transition scripts, temporary build artifacts, sensitive configuration files, or draft files that are no longer needed for regular development and production.

---

## 🗑️ Category 1: One-Off Transition Scripts (Tracked in Git)
These scripts were used for renaming/migrating codebase references from the old name (**VaaniSeva**) to **JanAI**. Since the rebranding is fully complete, these files are no longer needed.

| File Path | Description | Recommended Action | Status |
|:---|:---|:---|:---|
| [`replace.py`](file:///d:/Downloads/JanAI/JanAI/replace.py) | Python script for replacing branding strings in source code. | **Delete** | ❌ **Deleted** |
| [`website/fix_frontend.py`](file:///d:/Downloads/JanAI/JanAI/website/fix_frontend.py) | Python script for renaming frontend components and updating imports. | **Delete** | ❌ **Deleted** |
| [`website/fix_frontend.cjs`](file:///d:/Downloads/JanAI/JanAI/website/fix_frontend.cjs) | CommonJS script used for renaming and replacing text in frontend assets. | **Delete** | ❌ **Deleted** |
| [`scripts/cleanup_old_references.py`](file:///d:/Downloads/JanAI/JanAI/scripts/cleanup_old_references.py) | Cleanup script for S3 TTS caches and DynamoDB tables. Run once after migration. | **Delete** (or move to a `backup/` or `archive/` folder if needed for future reference) | ❌ **Deleted** |


---

## 📄 Category 2: Temporary and Query Snippets (Tracked in Git)
These files were accidentally tracked or created during development and contain temporary data or helper HTML.

| File Path | Description | Recommended Action |
|:---|:---|:---|
| [`website/filter.json`](file:///d:/Downloads/JanAI/JanAI/website/filter.json) | A DynamoDB query filter payload containing email addresses (`jatinkarmaa@gmail.com`). | **Delete** (contains hardcoded email reference) |
| [`JanAIIcons_Preview.html`](file:///d:/Downloads/JanAI/JanAI/JanAIIcons_Preview.html) | A local HTML file used to preview SVG icons. | **Delete** (rebuildable from React components if needed) |

---

## 🔒 Category 3: Sensitive Local Environment Files (Ignored/Untracked)
These files contain local API keys, database configurations, and AWS credentials. They should never be committed to Git. Most of these are correctly ignored by `.gitignore` but exist locally.

| File Path | Description | Recommended Action |
|:---|:---|:---|
| [`vercel_preview.env`](file:///d:/Downloads/JanAI/JanAI/vercel_preview.env) | Untracked Vercel environment variables for preview deployments. | **Keep locally (Do not commit)** |
| [`vercel_prod.env`](file:///d:/Downloads/JanAI/JanAI/vercel_prod.env) | Untracked Vercel environment variables for production deployments. | **Keep locally (Do not commit)** |
| [`.env`](file:///d:/Downloads/JanAI/JanAI/.env) | Local configuration environment variables. | **Keep locally (Do not commit)** |
| [`.env.local`](file:///d:/Downloads/JanAI/JanAI/.env.local) | Local overrides of configuration variables. | **Keep locally (Do not commit)** |
| [`website/.env.local`](file:///d:/Downloads/JanAI/JanAI/website/.env.local) | Local frontend override configurations. | **Keep locally (Do not commit)** |
| [`website/.env.vercel`](file:///d:/Downloads/JanAI/JanAI/website/.env.vercel) | Frontend environment variables for Vercel. | **Keep locally (Do not commit)** |
| [`website/.env.vercel.prod`](file:///d:/Downloads/JanAI/JanAI/website/.env.vercel.prod) | Frontend production environment variables for Vercel. | **Keep locally (Do not commit)** |

---

## 📝 Category 4: Leftover Drafts and Documentation (Ignored/Untracked)
These are developmental drafts or historical documents that are ignored by Git.

| File Path | Description | Recommended Action |
|:---|:---|:---|
| [`prd/contex.md`](file:///d:/Downloads/JanAI/JanAI/prd/contex.md) | An older/draft version of the Product Requirements Document (PRD) with a filename typo. The clean, correct version is `prd/JANAI_PRD.md`. | **Delete** |
| [`architecture_prompt.md`](file:///d:/Downloads/JanAI/JanAI/architecture_prompt.md) | Prompt script used to generate architecture layouts, no longer needed. | **Delete** |
| [`implementation_plan.md`](file:///d:/Downloads/JanAI/JanAI/implementation_plan.md) | Historical implementation plan for call responsiveness and pace fixes. | **Delete** |
| [`utils/`](file:///d:/Downloads/JanAI/JanAI/utils) | Contains several ignored markdown files (`DESIGN.md`, `HANDOFF.md`, `PPTCONTENT.MD`, `TEAM_TASKS.md`, `pptcreation.md`). | **Archive or Delete** if the information is already integrated into the main `README.md` or `prd/JANAI_PRD.md`. |

---

## ⚙️ Category 5: Build Caches, Dependencies, and OS Files (Ignored)
These directories are standard system-generated folders that should not be tracked and are currently ignored.

| Path | Description | Recommended Action |
|:---|:---|:---|
| `node_modules/`, `website/node_modules/` | Node package dependencies. | **Keep (Managed by npm)** |
| `venv/`, `.venv/` | Python virtual environment. | **Keep (Managed locally)** |
| `website/dist/` | Production build output for the React website. | **Safe to delete (rebuilt via `npm run build`)** |
| `.vercel/`, `website/.vercel/` | Vercel deployment cache files. | **Safe to delete (re-generated on deployment)** |
| `**/__pycache__/` | Python compiled bytecode caches. | **Safe to delete (auto-generated)** |
| `.DS_Store`, `Thumbs.db` | OS-specific folder preview metadata. | **Safe to delete** |

---

## 🧪 Category 6: Developer Testing Scripts (Safe, but Optional to Upload)
These scripts are located under the `scripts/` folder. They are used to test and debug individual parts of the system.

### Are they safe to upload?
*   **Yes.** They do **not** contain any hardcoded API keys or AWS credentials. They load all credentials dynamically from the local `.env` file via `dotenv`.

### Should you upload them for the hackathon submission?
*   **Highly Recommended:** Keeping these files is usually preferred because it allows judges or other team members to verify that the environment has been set up correctly by running test commands (e.g., verifying their Bedrock access works).
*   **Optional:** If you want a 100% minimal production repository without developer diagnostic tools, you can add them to `.gitignore` or delete them.

| File Path | Purpose |
|:---|:---|
| [`scripts/test_aws_access.py`](file:///d:/Downloads/JanAI/JanAI/scripts/test_aws_access.py) | Verifies STS Caller Identity, S3 bucket listings, DynamoDB permissions, and Bedrock accessibility. |
| [`scripts/test_bedrock.py`](file:///d:/Downloads/JanAI/JanAI/scripts/test_bedrock.py) | Tests Claude 3.5 Sonnet prompt completion and Titan Embeddings generation. |
| [`scripts/test_call.py`](file:///d:/Downloads/JanAI/JanAI/scripts/test_call.py) | Triggers outbound Twilio call routing through the live API Gateway/Lambda webhook for demonstration. |
| [`scripts/test_elevenlabs.py`](file:///d:/Downloads/JanAI/JanAI/scripts/test_elevenlabs.py) | Tests character count, voice availability, and latency comparisons with ElevenLabs. |
| [`scripts/test_voices.py`](file:///d:/Downloads/JanAI/JanAI/scripts/test_voices.py) | Local utility to preview and play all available Sarvam AI bulbul:v2 voices. |

---

## 🧹 Quick Cleanup Command
To safely remove only the **unwanted tracked scripts, temp filters, and duplicate markdown drafts** (without affecting your local `.env` keys, virtual environments, or `node_modules`), you can run the following PowerShell command in the project root:

```powershell
# Remove unwanted tracked and temporary files
Remove-Item -Path "replace.py", "website/fix_frontend.py", "website/fix_frontend.cjs", "website/filter.json", "JanAIIcons_Preview.html", "prd/contex.md", "architecture_prompt.md", "implementation_plan.md" -Force -ErrorAction SilentlyContinue
```
