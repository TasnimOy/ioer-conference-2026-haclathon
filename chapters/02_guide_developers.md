---
title: Guide for Developers (Jupyter & Git)
---

# Guide for Developers (Jupyter & Git)

Welcome! If you are contributing Python/R code, spatial analyses, or interactive maps (e.g., MapLibre), you will be working directly with Jupyter Notebooks (`.ipynb`).

## 1. Setting up your Computing Environment

### Option A: Cloud Start

> Jupyter4NFDI - Easiest!

Run this repository interactively in your browser via the **Jupyter4NFDI Hub**.
- Click the 🚀 icon in the top menu bar of this book's [start page](https://hack.conference.ioer.info/) and select "Jupyter4NFDI".
- Authenticate using the Helmholtz AAI. 
  *(Note for international participants: Helmholtz AAI allows you to log in using social identities like GitHub, Google, or ORCID if you don't have an institutional account!)*
- The environment will load with JupyterLab, Git, and all base dependencies pre-installed.

### Option B: Local Start
> Carto-Lab Docker

For local reproducibility, use the IOER FDZ [Carto-Lab Docker](https://cartolab.fdz.ioer.info/) (or any JupyterLab environment).
```bash
git clone https://gitlab.vgiscience.de/lbsn/tools/jupyterlab.git
cd jupyterlab
cp .env.example .env
docker network create lbsn-network
docker compose pull && docker compose up -d
```

## 2. How to Submit Your Work

You do not need to be a Git expert to submit your code. Choose the method that works best for you:

### Method 1: Download & Drop 
> no Git required

1. Work in your JupyterLab environment until you are happy with your notebook.
2. Right-click your `.ipynb` file in the left sidebar and select `Download`.
3. Upload your downloaded file to our [File Folder Drop (Datashare)](https://datashare.tu-dresden.de/s/XeBH775Pa8L5CiG).
4. Send a quick email to `fdz@ioer.de` to let us know it's there. We will integrate it into the book!

### Method 2: Git Workflow

If you are comfortable with Git:

1. **Fork** the [HaCLAthon GitHub Repository](https://github.com/ioer-dresden/ioer-conference-2026-haclathon).
2. **Develop** your `.ipynb` notebook in the `notebooks/` directory.
3. Ensure **Jupytext** has synced your `.md` file before committing.
4. **Push** your changes (Requires a GitHub Personal Access Token if pushing from the cloud).
5. **Open a Pull Request** against our `main` branch.

Have a look at our [developer notes for working with git](https://hack.conference.ioer.info/DEVELOPERS.html#jupyter-collaborative-editing).

## 3. Integrating External Web-Maps and Dashboards 
> e.g., MapLibre/Leaflet

If you have built a custom JavaScript map or Storymap (or a standalone dashboard etc.), you can embed it into a Jupyter Book chapter without causing script conflicts:

1. Save your map as a standalone HTML file (e.g., `storymap.html`).
2. Upload it alongside your notebook.
3. In your Jupyter Notebook, use an `IFrame` to display it:

```python
from IPython.display import IFrame
# Display the external map seamlessly inside the book
IFrame(src="./storymap.html", width="100%", height="700px")
```