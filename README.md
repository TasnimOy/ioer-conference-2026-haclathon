[![version](https://hack.conference.ioer.info/version.svg)][static-gl-url] [![pipeline](https://hack.conference.ioer.info/pipeline.svg)][static-gl-url] [![doi](https://hack.conference.ioer.info/doi.svg)][doi-url]

# Sustainability Transformation HaCLAthon (IOER Conference 2026)

Welcome to the collaborative workspace for the **Sustainability Transformation HaCLAthon** (Contribution Format F5 of the 4th IOER Conference "Space & Transformation").

## What is a HaCLAthon?

Unlike traditional hackathons, this project is a **C**ollaborative, **L**ong-term, and **A**synchronous data challenge. Participants contribute code, visualizations, and workflows over several months. The result is a living **Jupyter Book**, which will be archived as a citable **data publication** with a DOI.

**View the Living Book:** [https://hack.conference.ioer.info/](https://hack.conference.ioer.info/)

---

## How to Participate

We welcome contributions from both domain experts (text/concepts) and data scientists (code/maps). Please choose the path that fits your background:

### Path A: The Writer (No coding required)

Best for text-based stories, conceptual contributions, and data narratives.
*   **Tool:** Use our browser-based [Collaborative Editor](https://hack.conference.ioer.info/editor/).
*   **Workflow:** [Read the Guide for Writers](https://hack.conference.ioer.info/chapters/01_guide_writers.html).

### Path B: The Developer (Jupyter & Git)

Best for Python/R analysis, API integration, and interactive visualizations.
*   **Tool:** Jupyter Notebooks via [Jupyter4NFDI](https://hub.nfdi-jupyter.de/) or [Carto-Lab Docker](https://cartolab.fdz.ioer.info/).
*   **Workflow:** [Read the Guide for Developers](https://hack.conference.ioer.info/chapters/02_guide_developers.html).

---

## Infrastructure & Collaboration

*   **Public Mirror:** This GitHub repository serves as our primary intake for community Pull Requests.
*   **Single Point of Truth:** Internal collaboration and CI/CD building take place in our [GitLab repository][static-gl-url].
*   **Versioning:** This project is versioned with [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/).

 ```mermaid 
 %%{init: { 'theme':'forest', 'securityLevel': 'loose', 'sequence': {'useMaxWidth':false} } }%%
 flowchart LR;
    Source[Notebooks/Markdown]-->CI[GitLab-CI]-->Build[Jupyter Book]-->Web[hack.conference.ioer.info]
 ```

For a detailed walkthrough, see the [Quick-Start Guide](https://hack.conference.ioer.info/chapters/00_quickstart.html).

[1]: https://hack.conference.ioer.info/chapters/02_guide_developers.html#carto-lab-docker
[static-gl-url]: https://gitlab.hrz.tu-chemnitz.de/ioer/fdz/training/hackathon-ioer-conference-2026
[doi-url]: https://tbd
