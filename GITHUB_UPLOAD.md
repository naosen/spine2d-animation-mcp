# Uploading SPINE2D Animation MCP Server to GitHub

This guide walks you through the process of uploading this project to GitHub.

## Prerequisites

1. A GitHub account
2. Git installed on your computer
3. Basic familiarity with Git commands

## Step 1: Create a New GitHub Repository

1. Log in to your GitHub account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Enter a repository name (e.g., "spine2d-animation-mcp")
4. Add a description (optional)
5. Choose public or private visibility
6. Do NOT initialize the repository with a README, .gitignore, or license (we already have these files)
7. Click "Create repository"

## Step 2: Initialize Git in Your Local Project

Open a terminal and navigate to your project directory:

```bash
cd /Users/eli/Desktop/spine2d-animation-mcp
```

Initialize Git:

```bash
git init
```

## Step 3: Add Your Files to Git

Stage all files for commit:

```bash
git add .
```

Commit the files:

```bash
git commit -m "Initial commit of SPINE2D Animation MCP Server"
```

## Step 4: Connect Your Local Repository to GitHub

Add the GitHub repository as a remote:

```bash
git remote add origin https://github.com/YOUR_USERNAME/spine2d-animation-mcp.git
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 5: Push Your Code to GitHub

Push your committed code to GitHub:

```bash
git push -u origin main
```

Note: If your default branch is named "master" instead of "main", use:

```bash
git push -u origin master
```

## Step 6: Verify Your Repository

1. Go to your GitHub profile
2. Navigate to the repository you just created
3. Confirm that your files have been uploaded successfully

## Additional Tips

### Adding a Description and Topics

1. Navigate to your repository on GitHub
2. Click the gear icon next to "About" on the right side
3. Add a description, website (if applicable), and topics (e.g., "spine2d", "animation", "mcp", "ai-animation")
4. Click "Save changes"

### Setting Up GitHub Pages (Optional)

If you want to create a project website:

1. Go to your repository's "Settings" tab
2. Scroll down to "GitHub Pages"
3. Under "Source", select "main" branch and "/docs" folder (you would need to create a docs folder with HTML files)
4. Click "Save"

### Protecting Your Main Branch (Optional)

1. Go to your repository's "Settings" tab
2. Click on "Branches" in the left sidebar
3. Under "Branch protection rules", click "Add rule"
4. Enter "main" (or "master") as the branch name pattern
5. Choose your protection settings (e.g., require pull request reviews)
6. Click "Create"

## Updating Your Repository

After making changes to your local code:

```bash
git add .
git commit -m "Description of changes"
git push
```

## Collaborating with Others

Share your GitHub repository URL with collaborators. They can clone your repository:

```bash
git clone https://github.com/YOUR_USERNAME/spine2d-animation-mcp.git
```

They can then make changes, commit them, and create pull requests for you to review.