# Guide for Writers (Browser Editor)

If you want to contribute concepts, text, or data stories to the **HaCLAthon** without worrying about coding environments or Git, this path is for you.

We use a visual, browser-based editor. Your changes are automatically converted into Pull Requests and reviewed by our editorial team.

## Step 1: Getting Access

To ensure scientific integrity, our workspace is invite-only.
1. If you don't already have one, create a free account on [GitHub.com](https://github.com/).
2. You need to send us your GitHub username and a brief description of your planned contribution. You can do this through several channels:
    - Send an email to [fdz@ioer.de](mailto:fdz@ioer.de)
    - Join our HaCLAthon Matrix Channel (e.g. through Element): [https://matrix.to/#/#HaCLAthon:tu-dresden.de](https://matrix.to/#/#HaCLAthon:tu-dresden.de)
    - Create an [Issue on Github in our public HaCLAthon Repository](https://github.com/ioer-dresden/ioer-conference-2026-haclathon/issues)
4. We will add you as a "Collaborator". You will receive an email from GitHub. **You must click "Accept Invitation" in that email.**

```{figure} ../resources/2026-05-06_invitation.webp
:name: Invitation

Invitation visible when viewing the [Github Repository of the HaCLAthon](https://github.com/ioer-dresden/ioer-conference-2026-haclathon/).
```

## Step 2: Logging In

Once you have accepted the invitation:
1. Click the **[Collaborative Editor](/editor/)** link.
2. Click **"Sign in with GitHub"** and authorize the IOER application.
*(Note: We do not see your password. The login is processed securely via our institute broker).*

```{figure} ../resources/2026-05-06_oauth_cms.webp
:name: Sveltia/Decap Login Screen
:figclass: fig-no-shadow

Sign-in through our Github integration for live-edit of chapters.
```

## Step 3: The Editorial Workflow

When you log in, you will see a Kanban board with three columns: **Drafts**, **In Review**, and **Ready**.
This is our "Editorial Inbox". 

* To create a new chapter, click **"New Book Chapter"**.
* To edit an existing chapter, click on its name in the board.

```{figure} ../resources/workflow.webp
:name: Editor Workflow

Editorial Inbox Workflow in Live Editor.
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
If you want to read more about style conventions that you can use to format your chapter, have a look at our full [Developers](../DEVELOPERS#formatting-conventions) Section.
```
