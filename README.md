# Cajamar – Decision Tree Classifier (Watson Studio)

Trains a scikit-learn `DecisionTreeClassifier` from data in IBM Cloud Object Storage and
registers it as a model asset in a Watson Studio project through Watson Machine Learning.

## Repository layout

```
assets/
  jupyterlab/
    train_classifier.py   # notebooks and scripts live here
requirements.txt
.gitignore
```

Watson Studio requirements this layout follows:

- **Deprecated Git integration (with sync):** only files under `assets/jupyterlab/` (or its
  subfolders) are pushed, pulled and synced as notebook/script assets. Use regular `.py`
  files; `.ipy` files are not synced.
- **Default Git integration:** no directory restriction, but `assets/` is reserved for
  project asset files, so don't save your own files under `assets/` outside `jupyterlab/`.
- One repository per project. Don't reuse a repository across default and deprecated Git
  projects, or across two JupyterLab projects.
- Python functions are not supported in Git-integrated projects.
- For Git integration with the project (sync, JupyterLab, project terminal), see the IBM
  docs "Accessing a Git repository" and "Syncing Git changes with your project". It is
  available on IBM software deployments (Cloud Pak for Data / IBM Software Hub), not on
  IBM Cloud SaaS, where you can only publish notebooks to GitHub
  (Manage > Services and integrations > Third-party integrations, token with `repo` and
  `gist` scopes).

## Connecting the repository

1. Push this repository to GitHub (use an empty repository for a new deprecated-Git project;
   all existing files in it are deleted on project creation).
2. Create a personal access token with the `repo` scope.
3. In Watson Studio, create a new project, select **Git integration**, enter the token and
   repository URL, and choose the branch (`main`).
4. Launch JupyterLab from the project; files are under `assets/jupyterlab/`.
5. After pushing from an external Git client, use the project **Sync** icon to pull changes.

## Configuration (environment variables)

Secrets are never stored in the repository. Define these in the project environment or job:

| Variable | Required | Description |
|---|---|---|
| `PROJECT_ID` | yes | Watson Studio project ID (set automatically inside the project runtime) |
| `WML_API_KEY` | yes | IBM Cloud API key for Watson Machine Learning |
| `COS_API_KEY` | yes | IBM Cloud API key for Cloud Object Storage |
| `COS_INSTANCE_CRN` | yes | COS service instance CRN |
| `WML_URL` | no | Default `https://eu-de.ml.cloud.ibm.com` |
| `COS_ENDPOINT` | no | Default `https://s3.us-south.cloud-object-storage.appdomain.cloud` |
| `COS_BUCKET` | no | Default `cicd-bucket-test` |
| `COS_OBJECT_KEY` | no | Default `pre.xlsx` |

Install dependencies with `pip install -r requirements.txt` if the runtime lacks them.
