---
title: Guide for Writers (Browser Editor)
---

# Guide for Writers (Browser Editor)

If you want to contribute concepts, text, or data stories to the **HaCLAthon** directly in your browser, this path is for you.

We use a visual, browser-based editor (Decap CMS). Your changes are automatically converted into Pull Requests and reviewed by our editorial team.

```{admonition} No GitHub account?
:class: tip
The visual editor requires a GitHub account. If you prefer not to create one, simply write your text in Microsoft Word, Google Docs, or a raw `.md` file, upload it to our [File Drop Folder](https://datashare.tu-dresden.de/s/XeBH775Pa8L5CiG) and write an Email to us. We will format it and add it to the book for you!
```

## Step 1: Getting Access
To use the visual editor, we need to add you to the [ioer-conference-2026-haclathon](https://github.com/ioer-dresden/ioer-conference-2026-haclathon/) repository as a contributor.
1. Create a free account on [GitHub.com](https://github.com/).
2. Email us at [fdz@ioer.de](mailto:fdz@ioer.de) with your GitHub username.
3. You will receive an email invitation from GitHub. Click "Accept Invitation".

```{figure} ../resources/2026-05-06_invitation.webp
:name: Invitation

Invitation visible when viewing the [Github Repository of the HaCLAthon](https://github.com/ioer-dresden/ioer-conference-2026-haclathon/).
```

## Step 2: Logging In

Once you have accepted the invitation:
1. Click the <strong><a href="/editor/">Collaborative Editor</a></strong> link.
2. Click **"Sign in with GitHub"** and authorize the IOER application.
*(Note: We do not see your password. The login is processed securely via our institute broker).*

```{figure} ../resources/2026-05-06_oauth_cms.webp
:name: Sveltia/Decap Login Screen
:figclass: fig-no-shadow

Sign-in through our Github integration for live-edit of chapters.
```

## Step 3: Editorial Workflow

When you log in, you will see a Kanban board with three columns: **Drafts**, **In Review**, and **Ready**.
This is our "Editorial Inbox". 

* To create a new chapter, click **"New Book Chapter"**.
* To edit an existing chapter, click on its name in the board.

```{figure} ../resources/workflow.webp
:name: Editor Workflow

Editorial Inbox Workflow in Live Editor.
```

```{figure} ../resources/overview.webp
:name: Editor Overview

List of existing chapters (excluding data notebooks).
```

## Step 4: Writing and Formatting

The editor uses Markdown, a simple text-formatting language. You can use the formatting toolbar at the top (for Bold, Italic, Lists) or type Markdown directly.

```{figure} ../resources/2026-05-06_editor.webp
:name: Live Editor

Editor for live-editing contributions (Text, Images etc.).
```

**Adding Images:**
You can easily add images to your text.
1. Click the `+` icon in the toolbar and select "Image".
2. Upload your image from your computer. The system will automatically place it in our `resources/` folder and insert the correct code into your text.

```{figure} ../resources/image.webp
:name: Add Images

Image form (to be filled) after clicking `+` icon in the toolbar.
```

## Step 5: Submitting for Review

When you are finished writing:
1. Click **Save**.
2. Change the status from **"Draft"** to **"In Review"**.
3. This alerts the IOER conference curation team. We will review your text, format it into the Jupyter Book, and publish it to the live website!

You can view your changes, after they have been reviewed and merged, at https://hack.conference.ioer.info.

## Step 6: Iterate

Please publish often, even if your chapter is not fully ready. The HaCLAthon is specifically made for live collaboration and we welcome incremental contributions!
When we merged changes, you can re-open the editor and continue where you left. This will create an iterative contribution workflow of incremental steps that will once lead to the final HaCLAthon book.

```{admonition} Style guidelines. 
:class: tip
If you want to read more about style conventions that you can use to format your chapter, have a look at our full [Developers](content:references:formattingconventions) Section.
```
