---
title: Settlement Delineation with IBTool
---

# Settlement Delineation with IBTool: Testing and Improving an Automated § 34 BauGB Boundary

* **Author**: Oliver Harig
* **Topics**: Settlement Monitoring, Urban & Regional Planning, Open Source Tooling, QGIS
* **Skill profile**: QGIS users and domain experts — **no programming knowledge required**
*  **Badges**: ![Tutorial](https://img.shields.io/badge/Type-Workflow_Tutorial-green?style=flat-square) ![QGIS](https://img.shields.io/badge/Software-QGIS_3.x-589632?style=flat-square&logo=qgis&logoColor=white) ![No Python](https://img.shields.io/badge/Execution-Hands--on_Guide-lightgrey?style=flat-square)

```{admonition} Summary
:class: hint

Where exactly does a settlement end? In German planning law the answer decides whether a plot may be built on without a development plan (§ 34 BauGB, *Innenbereich*), yet in practice the boundary is usually digitised by hand or borrowed from administrative geometries. **IBTool** is an open-source QGIS plugin that derives this boundary automatically from building footprints, the road network and topographic data ({cite:alp}`ijgi10050353`). This chapter gives you the context, walks you through installing and running the three plugins of the toolchain, explains every processing parameter — and then hands you the actual work: **run it, break it, tune it, improve it, and document what you find as GitHub issues we discuss together.**
```

---

## 1. Context: Why an Automated Settlement Boundary?

### 1.1 The planning problem

German building law distinguishes between the *Innenbereich* (§ 34 BauGB — the coherently built-up area, where infill development is generally permissible without a development plan) and the *Außenbereich* (§ 35 BauGB — the open landscape, where building is heavily restricted). The line between the two is only in very few cases drawn by statute. It is established case by case, from the actual built structure on the ground.

That has three practical consequences:

* **It is expensive.** Municipalities digitise the boundary manually, plot by plot. For a whole federal state this is not feasible.
* **It is inconsistent.** Two planners drawing the same village produce two different boundaries. Boundaries drawn ten years apart are not comparable, so time series break.
* **The substitutes are not substitutes.** Administrative or land-use geometries (ATKIS® *Ortslage*, GHSL, municipal boundaries) are readily available but were built for other purposes. They over-detect at settlement edges and miss the fine-grained structure that infill analysis depends on.

### 1.2 Why this matters beyond the individual municipality

A consistent, reproducible settlement boundary is the base layer for a whole family of monitoring questions:

* **Settlement-area monitoring** — how much settlement area exists, and how is it changing?
* **Infill potential (*Innenentwicklungspotenzial*)** — which undeveloped plots lie *inside* the settlement and could absorb growth without consuming new land?
* **Land take reporting** — tracking progress against land consumption reduction targets requires a stable definition of "settlement" across years and across states.
* **Sprawl and density indicators** — most of them are only as good as the boundary they are computed against.

Because the delineation is derived purely from data, it scales: the same rules can be applied to a single municipality or to all of Germany, and re-run next year on new data to produce a genuinely comparable time series.

### 1.3 Does it work?

IBTool implements the method published in {cite:alp}`ijgi10050353`. A later independent, structured web- and GIS-based expert evaluation ({cite:alp}`repec:sae:envirb:v:52:y:2025:i:7:p:1735-1755`) compared automated delineations against established products and found IBTool's boundaries **more precise and more consistent than ATKIS® *Ortslage* and GHSL, with notably less over-detection at settlement edges**.

"Better than the alternatives" is not the same as "good enough everywhere", though. The method was calibrated on specific regions and specific data, and its defaults encode assumptions — about what counts as a building, how large a building gap may be, how dense a block must be. **Testing those assumptions against your own region is exactly what this chapter asks you to do.**

```{admonition} What this chapter is not
:class: note
This is not a Jupyter notebook. IBTool is a graphical QGIS plugin — everything below happens in the QGIS interface, not in Python. You need to be able to load layers, check a CRS and read an attribute table. You do **not** need to read or write code.
```

---

## 2. The Toolchain: Three Plugins

IBTool needs five inputs, and two companion plugins exist to produce them. All three are QGIS plugins by the same author and are installed the same way.

| Plugin | QGIS name | Role | Produces |
|---|---|---|---|
| **Data Wizard** | *IB-Tool-Data-Wizard* | Turns raw ATKIS Basis-DLM downloads into IBTool's input layers | `HU.gpkg`, `RN.gpkg`, `AUX_L.gpkg` |
| **Partitioning** | *IB-Tool (Partitioning)* | Splits the study area into processing units via kernel density + Voronoi | `PART_<id>` polygon layer |
| **IBTool** | *IB-Tool* | The delineation itself | Settlement boundary GeoPackage |

The intended order is:

```text
ATKIS raw data  ──Data Wizard──►  HU / RN / Aux
                                       │
HU  ──Partitioning──►  Part            │
                          └────────────┴──►  IBTool  ──►  settlement boundary
                                       ▲
                    filter file  ──────┘
```

The filter file is a small plain-text list of ATKIS building function codes, maintained by hand. It is the one input neither companion plugin produces — and, as you will see in Track B, the one that most often needs regional adaptation.

```{admonition} Repositories
:class: tip
All three plugins are public and live in the [`IB-Tool` GitHub organisation](https://github.com/IB-Tool). Source, documentation, releases and issue trackers are open — a GitHub account is only needed to open issues or comment.

* IBTool — [IB-Tool/IB-Tool-3](https://github.com/IB-Tool/IB-Tool-3)
* Data Wizard — [IB-Tool/data_wizard](https://github.com/IB-Tool/data_wizard)
* Partitioning — [IB-Tool/ibtoolpartion](https://github.com/IB-Tool/ibtoolpartion)

All three are licensed **GPL-2.0-or-later**.
```

---

## 3. Installation

### 3.1 Requirements

| Requirement | Minimum | Note |
|---|---|---|
| QGIS | 3.40 (tested to 3.50) | Data Wizard and Partitioning also run on older 3.x |
| Python | 3.11 | bundled with QGIS |
| `numpy`, `PyQt5` | — | bundled with QGIS, nothing to do |
| `scipy`, `networkx` | 1.11+ / 3.0+ | **not always bundled** — see below |

If IBTool shows a red message bar right after loading, `scipy` or `networkx` are missing. Install them once into QGIS's own Python:

```bash
Windows: Start Menu → OSGeo4W → OSGeo4W Shell
pip install scipy networkx

Linux / macOS: a terminal in which QGIS's Python is active
pip install scipy networkx
```

Then restart QGIS. If they are still reported missing, `pip` ran against a system Python rather than QGIS's — on Windows the OSGeo4W Shell sets the correct environment automatically.

### 3.2 Installing the plugins

For each plugin: download the release ZIP → **Plugins → Manage and Install Plugins… → Install from ZIP** → select the file → **Install Plugin** → tick the checkbox in the **Installed** tab.

```{admonition} Two installation traps — read before you download
:class: warning

1. **Download the right asset.** On the IBTool [Releases](https://github.com/IB-Tool/IB-Tool-3/releases) page, take the attached `IB-Tool-3.zip` asset — **not** GitHub's auto-generated *"Source code (zip)"*. The auto-generated archive is named after the release tag, which bakes the version number into the folder name, and QGIS then fails with `ModuleNotFoundError: No module named 'IB-Tool-3-0'`.
2. **The folder name may need renaming.** QGIS builds the plugin folder from the top-level folder in the ZIP and requires it to be a valid Python identifier — no hyphens, no leading digits. If *IB-Tool* does not appear after installing, go to your plugins folder and rename `IB-Tool-3` → `ibtool`, then restart QGIS. Data Wizard (`data_wizard`) and Partitioning (`ibtoolpartion`) are already valid identifiers and need no renaming.

| OS | Plugins folder |
|---|---|
| Windows | `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins` |
| Linux | `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins` |
| macOS | `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins` |
```

After installation the tools appear under **Plugins → IB-Tool** (Data Wizard is grouped there as well).

**Reference documentation:** [IBTool quickstart](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/quickstart.md) · [Data Wizard docs](https://github.com/IB-Tool/data_wizard/blob/master/docs/README.md) · [Partitioning README](https://github.com/IB-Tool/ibtoolpartion/blob/master/README.md)

---

## 4. Preparing the Input Data

### 4.1 What IBTool expects

Five inputs, **all in the same projected CRS** (plugin default: ETRS89 / UTM 33N, EPSG:25833):

| Input | Geometry | Min. features | Key requirement |
|---|---|---|---|
| **HU** — building footprints | Polygon | 50 | field `fkt`, `funktion` or `gfkzshh` with the ATKIS function code (e.g. `31001_1000`) |
| **RN** — road network | Line | 30 | single-part geometries only |
| **Part** — partitions | Polygon | 1 | field `NAME`, values matching `PART_<number>` |
| **Aux** — auxiliary lines | Line | 10 | forest / water / rail edges, merged with RN |
| **Filter file** | `.txt` | — | sections `#Filter positive` and `#Filter negative` |

Full specification and the complete validation checklist: [`docs/input-data.md`](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/input-data.md).

### 4.2 Fastest path: use the sample data

IBTool ships a ready-to-run dataset in `Testdaten/` (`A_HU.shp`, `A_RN.shp`, `A_PART.shp`, `A_AUX.shp`, `IB-Tool2_Filter.txt`), all in EPSG:25833 — matching the plugin default, so nothing has to be reprojected. **Start here.** Get one successful run behind you before you touch your own region.

### 4.3 Your own region: raw data → HU / RN / Aux

1. **Download ATKIS Basis-DLM** for your state. Portal, format and dataset names per state (Brandenburg, Sachsen, Sachsen-Anhalt, Berlin so far) are in [`docs/data-sources.md`](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/data-sources.md). Buildings come separately — ALKIS *Gebäude* or *Hausumringe*.
2. **Run Data Wizard.** Give it the folder with the seven raw shapefiles (`ver01_l`, `ver02_l`, `ver03_l`, `veg02_f`, `veg03_f`, `gew01_f`, `gew01_l`), the building file, optionally a study-area polygon to clip to, and a target folder. It fixes the project CRS from the raw data, reprojects anything that disagrees, clips, applies the fixed mapping rules and writes `HU.gpkg`, `RN.gpkg`, `AUX_L.gpkg`.
   * If the building file has no `fkt` / `gfkzshh` / `funktion` column, Data Wizard scans for a column matching the `31001_xxxx` pattern and copies it into a new `funktion` column — or asks you to pick the right one. Your source file is never modified.
   * The [manual QGIS workflow](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/data-preparation.md) this automates is documented step by step — worth reading once, so you know what the wizard is doing and can check its output.
3. **Run Partitioning** on your `HU` layer. Set the cell size (default 150 m; it drives both raster resolution and the density radius, which is `2 × cell_size`) and an output path. You get polygons named `PART_<id>`.

```{admonition} Draw the study area generously
:class: tip
Data Wizard clips exactly to your study-area polygon. Draw it noticeably **larger** than the area you actually care about, otherwise buildings and road segments are cut mid-feature right at the edge where the delineation matters most.
```

### 4.4 The filter file

A plain UTF-8 text file with two sections. Only the **first 10 characters** of each entry are matched against the building's function-code field:

```text
#Filter positive
31001_1000, Wohngeb
31001_1010, Wohnhaus
31001_1100, GemischtesWohnen
...

#Filter negative
31001_2721, Scheune
31001_2723, Schuppen
31001_2463, Garage
...
```

**Positive** = only buildings whose code appears here are kept. **Negative** = buildings whose code appears here are dropped. Conceptually this operationalises the legal distinction: a dwelling establishes a development context, a barn or a garage does not.

The shipped `IB-Tool2_Filter.txt` has 16 positive and 20 negative entries. It is deliberately small. **This is the file you are most likely to need to change** — see Track B.

---

## 5. Running IBTool

The dialog is a guided four-step workflow.

**Step 1 — Input.** Fill every path field with the **…** buttons. Fields turn green as files are found.

```{admonition} The output file must already exist — and be empty
:class: warning
Before starting, create an empty GeoPackage: QGIS Browser panel → right-click **GeoPackage** → **New GeoPackage File…**. Give it an **individual, descriptive name** (`result_dresden_p18_2026-08-15.gpkg`), not `output.gpkg`. IBTool overwrites the contents of whatever file you select. During a HaCLAthon, where several people work on the same sample data, a generic name is a guaranteed way to lose a result.
```

**Step 2 — Parameters.** Leave everything at default for the first run. Section 6 explains each one.

**Step 3 — Validation.** Click **Check**. You get a checklist: ✅ passed, ❌ error (blocks the run), ⚠️ warning (informational). **Start** stays grey until every error is resolved. The most common ones:

| Error | Fix |
|---|---|
| CRS mismatch | reproject all inputs to one CRS, and set that CRS in the dialog |
| Too few features | HU ≥ 50, RN ≥ 30, Aux ≥ 10 |
| Missing field | HU needs `fkt`, `funktion` or `gfkzshh`; Part needs `NAME` |
| Multipart geometries | `native:multiparttosingleparts` on RN and Aux |
| Part name format | values must match `PART_<number>` |

**Step 4 — Processing.** Click **Start**. Partitions are processed in sequence; the phase label, progress bar and log track the run. Afterwards: **Load result**, **Open folder**, **Export log**.

```{admonition} Turn on Debug Mode before you start investigating
:class: tip
The **Debug mode** checkbox writes a numbered GeoPackage snapshot after every processing module into `workspace/debug/<Module>/` — `001_after_positive_filter.gpkg`, `003_after_density_buffer.gpkg`, and so on. Load the folder into QGIS, sort by name, and step through the pipeline visually. This is by far the fastest way to find out *where* a result went wrong, and a debug snapshot attached to an issue is worth ten sentences of description.
```

---

## 6. Parameterisation

### 6.1 What the pipeline does

Each partition passes through ten steps ({cite:alp}`ijgi10050353`; full pseudocode in [`docs/how-it-works.md`](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/how-it-works.md)):

1. **Blocker** — derive street and city blocks from RN + Aux
2. **ImportFilter** — three-stage filter: function code → spatial density → minimum size
3. **FootprintDensity** — building coverage ratio (BCR) per block; dense blocks classified directly as settlement
4. **CreateMST** — Delaunay triangulation on building centroids → minimum spanning tree (Kruskal); road-crossing edges removed
5. **MST_Clustering** — group buildings into oriented minimum bounding rectangles, validated against a local BCR threshold
6. **AddSingleBuilding** — bounding rectangles for large isolated buildings (> 300 m²)
7. **EdgeCatch** — snap boundaries to the nearest road within 25 m
8. **ErodeEmptyAreas** — remove building-free voids (≥ 500 m²) enclosed in the polygon
9. **GapClose** — fill enclosed holes; bridge narrow gaps at the fringe
10. **PatchRemove** — drop splinter areas below size and building-count thresholds

### 6.2 Parameter reference

| Parameter | Default | Controls | Sensitivity |
|---|---|---|---|
| `min_overlap_blocks` | 18 % | BCR above which a block counts as densely developed and is assigned to the settlement directly | **high** |
| `global_footprint_density` | auto (0) | fallback reference BCR for the whole study area; decides how loose development is treated | **high** |
| `min_area` | 56.8 m² | buildings smaller than this are removed before anything else | low |
| `min_bdg_count` | 20 | minimum buildings for a patch to count as a locality | medium |
| `min_patch_size` | 10,000 m² | minimum area of a retained patch | medium |
| `max_hole_size` | 10,000 m² | largest enclosed open space still absorbed into the settlement | medium |
| `max_gap_size` | 4,900 m² | largest gap at the settlement edge that is bridged (≈ 70 m radius) | **high** |
| `footprint_density_threshold`* | 18 % | dense-block retention threshold inside PatchRemove | low |
| `footprint_area_sum`* | 6,000 m² | minimum total footprint area for a dense block to survive PatchRemove | low |

\* internal, not exposed in the UI.

### 6.3 The three that decide your result

**`min_overlap_blocks` (BCR threshold, default 18 %).** Blocks above this are settlement, full stop, and skip all later steps. Above ~25 % only compact town centres qualify; below ~15 % loose rural development is captured too. The empirically calibrated range is **18–22**. The default of 18 is deliberately conservative: it keeps false positives very low, at the cost of pushing more area into the expensive clustering steps.

**`max_gap_size` (default 4,900 m² ≈ 70 m).** The most contested parameter, because it encodes a genuinely contested legal question: how large may a building gap be and still count as *Innenbereich*? The algorithm only bridges an area if it borders settlement polygons along **at least 75 % of its perimeter** — contact with built-up land must clearly dominate contact with open land. Rule of thumb: the looser the surrounding development, the larger a legitimate gap can be. Recommended 40–100 m.

**`global_footprint_density` (default auto).** Leave on auto for homogeneous areas. Set it manually when your study area mixes very different settlement types — its influence on small and dispersed settlements is substantial.

Full derivation, mathematical background and the dissertation references: [`docs/parameterization.md`](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/parameterization.md).

---

## 7. Your Tasks

This is the actual work of the HaCLAthon. **Task A is the shared starting point** — everyone does it. After that, pick **one or more of the six tracks** in Section 7.2 according to your background, your data and the time you have. They are independent of each other; nobody is expected to do all of them. **Task Z runs alongside whatever you choose.**

### 7.1 Task A — Get a run through (everyone)

1. Run the sample data in `Testdaten/` with default parameters. Load the result next to `A_HU.shp` and look at it.
2. Prepare your own region (Data Wizard + Partitioning) and run it. If you have no data of your own, stay with the sample data — every track below works on it.
3. **Look critically.** Zoom to five or six places where you know the ground truth: a village edge, a farm, an industrial estate, a scattered hamlet, a large building gap. Where does the boundary do something you would not have done?

*Deliverable:* screenshots of two or three places where the result is convincing and two or three where it is not, with a one-line explanation each. This is also the material from which you choose your track.

### 7.2 Choose your track

| Track | What you work on | Effort | Needs own data? | Needs code? |
|---|---|---|---|---|
| **B — Filter file** | which buildings count as settlement-relevant | low–medium | helpful | no |
| **C — Parameters** | tuning the delineation to a settlement structure | medium | helpful | no |
| **D — Algorithm** | the delineation rules themselves | high | yes | optional |
| **E — Partitioning** | the upstream partitioning and its side effects | medium | no | no |
| **F — Data preparation** | Data Wizard for a new federal state | medium | yes | no |
| **G — Documentation & usability** | everything that trips up a first-time user | low | no | no |

---

#### Track B — Adapt the filter file

The shipped filter is a starting point, not a standard. Realistic reasons it will not fit your data:

* **Codes that occur in your region are missing entirely.** A code in neither list falls through — check what actually happens in your data rather than assuming.
* **Borderline building types.** Should a *Wochenendhaus* (currently negative) count in a region where holiday settlements are permanently inhabited? A *Gebäude für Wirtschaft oder Gewerbe* (currently positive) sitting alone in a field? A converted barn?
* **Your building data does not use `31001_xxxx` codes at all.** Some sources carry different classifications entirely.

**Do this:** build a frequency table of the function-code field of your `HU` layer (QGIS: right-click layer → **Properties → Fields**, or the statistics / *Group Stats* panel). Which codes are frequent in your region? Which are in neither filter section? Then adapt the file and re-run — same parameters, only the filter changed — and compare.

*Deliverable:* your adapted filter file, the frequency table, and a before/after comparison of the boundary.

---

#### Track C — Test the parameter settings

Vary parameters **one at a time**, keeping everything else fixed and using the same input data — otherwise you cannot attribute a change in the result to a cause.

Suggested series (start with the three high-sensitivity parameters):

| Parameter | Suggested values | Question |
|---|---|---|
| `min_overlap_blocks` | 14, 18, 22, 26 | At which threshold does your region's loose development stop being recognised? |
| `max_gap_size` | 1,600 / 4,900 / 10,000 m² (40 / 70 / 100 m) | Where does gap bridging start producing boundaries you would defend in a planning meeting — and where does it stop? |
| `min_bdg_count` | 10, 15, 20, 25 | At what point do the hamlets in your region disappear? |
| `min_patch_size` | 5,000 / 10,000 / 20,000 m² | Which real settlements get discarded as splinters? |

Give each run its own descriptively named output GeoPackage (`result_<region>_<param>_<value>.gpkg`) so the series stays traceable. A simple table of *parameter value → total settlement area → number of patches → your qualitative judgement* is already a valuable result.

*Deliverable:* the comparison table plus a recommendation — "for a settlement structure like mine, use X because Y".

---

#### Track D — Improve the delineation algorithm

The most demanding track, and the most interesting. Some concrete leads, each with the step it lives in:

* **`min_patch_size` ignores shape** (PatchRemove). A long thin ribbon of 10,000 m² and a compact block of 10,000 m² are treated identically. Would a compactness criterion be better?
* **The EdgeCatch snap distance is fixed at 25 m.** In areas with wide road corridors or few roads this either snaps too far or not at all. Should it scale with the local road density?
* **The 75 % perimeter rule in GapClose is a hard threshold.** Is it right? Should it depend on the density of the surrounding development, as the parameter documentation itself suggests?
* **`min_area` (56.8 m²) is a single national value.** Regional building stock differs considerably — a threshold derived from the local footprint-size distribution might work better than a constant.
* **MST edges are weighted by building-edge distance** and edges crossing roads are removed. Are there other barriers that should cut edges — watercourses, railways, steep terrain?
* **ErodeEmptyAreas removes voids ≥ 500 m².** In dense historic centres, are courtyards being eroded that a planner would count as *Innenbereich*?

You do not have to write code to contribute here. **A well-argued, well-documented case for why a rule fails, with data, is a complete contribution** — it is what a developer needs to fix it. If you do want to prototype, [`docs/how-it-works.md`](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/how-it-works.md) gives the pseudocode per step and the debug snapshots give you the intermediate geometries to work against.

*Deliverable:* a described failure case with data, a hypothesis about the cause, and a proposed rule change.

---

#### Track E — Test the partitioning

Partitioning is upstream of everything else and gets little attention — but IBTool processes each partition **independently**, so the partition layout can leave traces in the final boundary.

The only parameter is **cell size** (default 150 m), which drives both the raster resolution of the kernel density estimate and the density radius (`2 × cell_size`).

**Do this:**

1. Run Partitioning on the same `HU` layer with e.g. 100 / 150 / 250 / 400 m and compare the resulting partition layers: how many partitions, how large, do the boundaries fall in sensible places (open landscape) or do they cut through settlements?
2. Run IBTool with identical parameters on two different partitionings of the same area. **Look specifically along the partition borders** in the result: are there steps, breaks or duplicated edges where two partitions meet?
3. Note the runtime. `input-data.md` warns that the Part:HU ratio should not exceed 1:10,000 — few, large partitions mean very long per-partition runtimes. Where does the trade-off between runtime and boundary artefacts actually sit for your data?

*Deliverable:* a comparison of the partitionings, screenshots of any artefacts along partition borders, and a cell-size recommendation with a rationale.

---

#### Track F — Data preparation for a new federal state

[`docs/data-sources.md`](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/data-sources.md) currently documents four states: Brandenburg, Sachsen, Sachsen-Anhalt and Berlin. The ATKIS/AAA object schema is nationally standardised — but portals, download formats, dataset names and packaging are not. Data Wizard expects exactly seven shapefiles (`ver01_l`, `ver02_l`, `ver03_l`, `veg02_f`, `veg03_f`, `gew01_f`, `gew01_l`), flat in one folder.

**Do this** for a state that is not yet documented:

1. Download the ATKIS Basis-DLM and the building data (ALKIS *Gebäude* / *Hausumringe*). Note the portal, whether registration is required, the format offered, and how the data is packaged.
2. Feed it to Data Wizard. Does the layer naming match? Is anything missing, differently named, or split into more files? Does the CRS detection from `ver01_l.shp` work?
3. Check the output: does `HU.gpkg` carry a usable function-code field, or did the picker dialog have to step in? Are the `veg03_f` OBJART codes (43005/43006) present in this state's data?
4. Then run IBTool on the result and confirm the **Check** step passes.

*Deliverable:* a new section for `data-sources.md` in the same table format as the existing four, plus a note on every point where the wizard's fixed assumptions did not hold for this state. Both are directly mergeable contributions.

---

#### Track G — Documentation and usability

The lowest-threshold track, and disproportionately useful — the author cannot see his own tool with fresh eyes any more.

**Do this:** work through [`quickstart.md`](https://github.com/IB-Tool/IB-Tool-3/blob/master/docs/quickstart.md) strictly as written, from a QGIS without the plugins installed, and write down **every single point where you hesitate, guess or get stuck**. Specifically:

* Steps that are missing, out of order, or assume knowledge that is not stated.
* Error messages that do not tell you what to actually do next.
* UI labels that do not match the documentation (the German translation is loaded automatically when your QGIS locale is German — do the German labels match `input-data.md`'s translation table?).
* Places where a default value is not explained, or where you cannot tell what a field expects.
* Anything that made you look into the source code to answer a question — that is a documentation gap by definition.

Do not tidy anything up in your head while you read. "This was obvious once I understood X" is precisely the finding worth writing down.

*Deliverable:* a list of concrete points with the file and section they belong to. Suggested wording, if you have it, is welcome but not required.

---

### 7.3 Task Z — Document findings as issues, then discuss (all tracks)

Everything you find in Task A and in your track goes into a GitHub issue, in the repository of the tool concerned:

* IBTool → [IB-Tool/IB-Tool-3/issues](https://github.com/IB-Tool/IB-Tool-3/issues)
* Data Wizard → [IB-Tool/data_wizard/issues](https://github.com/IB-Tool/data_wizard/issues)
* Partitioning → [IB-Tool/ibtoolpartion/issues](https://github.com/IB-Tool/ibtoolpartion/issues)

The repositories are public, so anyone with a GitHub account can open an issue and comment — no invitation needed.

**One finding = one issue.** Bundled issues cannot be closed individually and tend to stall.

#### What makes an issue actionable

| Section | Content |
|---|---|
| **Title** | The symptom in one line — "GapClose bridges a 60 m gap across a stream in PART_112", not "GapClose broken" |
| **Environment** | Plugin version (from `metadata.txt` or the QGIS plugin manager), QGIS version, operating system |
| **Data** | Region, data source, CRS, roughly how many buildings. Attach a small extract if the licence allows it — this is usually the difference between an issue that gets fixed and one that does not |
| **Parameters** | The full parameter set of the run. Copy the values from Step 2, or attach your `CONFIG.ini` |
| **Expected vs. actual** | What you expected as a domain expert, what the tool produced, and **why your expectation is the right one** — that reasoning is the part only you can supply |
| **Evidence** | Screenshot with visible context, the relevant debug snapshot from `workspace/debug/<Module>/`, and the exported log |
| **Classification** | Bug / wrong result / documentation gap / feature request — say which you think it is |

Suggested labels: `ibtool` · `data-wizard` · `partitioning` · `bug` · `parameterisation` · `filter` · `algorithm` · `docs`.

#### Then discuss

Use the issue thread. Domain questions — "should a *Wochenendhaus* count as *Innenbereich*?" — usually have no single correct answer, and the discussion is the point: it makes the assumption baked into a default value explicit, and documents *why* the tool behaves as it does. That record is itself a result of the HaCLAthon, whether or not the code changes afterwards.

---

## 8. What a Good Contribution Looks Like

A useful contribution is **one track carried through properly**, not all six touched lightly. Concretely, that means:

* **Task A done and documented** — a run you can reproduce, with the input data and parameter set written down, and a handful of places you looked at closely.
* **The deliverable of your track** — the adapted filter file, the parameter comparison, the failure case, the cell-size recommendation, the new `data-sources.md` section, or the usability list.
* **Three to five well-documented issues** with data, evidence and an argued expectation. Two good issues beat ten one-liners.
* Ideally **one discussion thread** about a substantive delineation question that reveals where the method and planning practice diverge.

Only Track D benefits from programming, and even there it is optional. Everything else requires exactly the thing that is hardest to automate: someone who knows what the boundary *should* look like on the ground.

---

## References

```{bibliography}
:style: unsrt
:filter: docname in docnames
```
