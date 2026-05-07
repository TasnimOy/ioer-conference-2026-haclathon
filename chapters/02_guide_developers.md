---
title: Guide for Developers (Jupyter & Git)
---

# Guide for Developers (Jupyter & Git)

Welcome! If you are contributing Python/R code, spatial analyses, or interactive maps, you will be working directly with **Jupyter Notebooks (`.ipynb`)** and **Git**.

The HaCLAthon relies on the **FAIR principles** and reproducibility. This guide outlines our technical setup and contribution workflow.

## 1. The Core Workflow

Because we use an automated Continuous Integration (CI) pipeline to build this book, we ask developers to follow a standard "Fork & Pull" workflow:

1. **Fork** the [HaCLAthon GitHub Repository](https://github.com/ioer-dresden/ioer-conference-2026-haclathon).
2. **Clone** your fork locally or open it in a cloud environment.
3. **Create a branch** for your feature (e.g., `feat/urban-heat-map`).
4. **Develop** your `.ipynb` notebook in the `notebooks/` directory.
5. **Commit and Push** your changes to your fork.
6. **Open a Pull Request** against our `main` branch.

## 2. Setting up your Computing Environment

To avoid dependency conflicts, we highly recommend using one of our standardized environments.

### Option A: Cloud Execution (Jupyter4NFDI)

You can run this repository interactively in your browser via the **Jupyter4NFDI Hub**.
* Click the 🚀 icon in the top menu bar of this book and select "Binder".
* Authenticate using the Helmholtz AAI (IOER members can use "TU Dresden").
* The environment will load with all base dependencies pre-installed.

### Option B: Local Execution (Carto-Lab Docker)

For full local reproducibility, we use the IOER FDZ [Carto-Lab Docker](https://cartolab.fdz.ioer.info/). This contains a Linux base, JupyterLab, and all major cartographic Python packages.

```bash
git clone https://gitlab.vgiscience.de/lbsn/tools/jupyterlab.git
cd jupyterlab
cp .env.example .env
# Edit .env to set the TAG to our current version
docker network create lbsn-network
docker compose pull && docker compose up -d
```

## 3. Important: The Jupytext Sync

This repository uses **Jupytext** to maintain a bidirectional sync between `.ipynb` files and `.md` files.

* **Never edit the `.md` version of your notebook manually.** 
* Write your code in the `.ipynb` file. 
* Before committing, ensure Jupytext has synced your notebook. Our CI pipeline enforces consistency; if the `.md` and `.ipynb` files are out of sync, the build will fail.

## 4. Commit Message Conventions

Our Continuous Integration automatically builds versions and changelogs based on commit messages. Please use the [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/):

* `feat: added interactive folium map to chapter 3` (Creates a minor release)
* `fix: resolved legend overlay issue in heat map` (Creates a patch release)
* `docs: fixed typo in API instructions` (No version bump)

## 5. Cross-References and Citations

* **Literature:** Add your references to the `references.bib` file. Cite them in your notebook using `{cite:t}` or `{cite:p}`.
* **Anchors:** Do not rely on header names for linking. Define explicit targets above your headers `(my-anchor)=` and link to them using `[Link Text](my-anchor)`.

```{admonition} Style guidelines and system design. 
:class: tip
You can read the full info on our system design, including contribution guidelines and formatting style conventions that we try to adhere, in our [Developers](../DEVELOPERS) section.
```

