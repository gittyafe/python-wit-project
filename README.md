# Wit - A Version Control System

Wit is a lightweight version control system inspired by Git, designed for tracking changes to files and managing different versions of your project.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Navigate to the project directory:
```bash
cd path/python wit project
```

2. Run this command in the cmd, as administrator
```bash
pip install -e .
```

This will install the `wit` command-line tool and its dependencies (Click).

## Quick Start

After installation, you can use wit by typing `wit` followed by a command in your terminal.

## Commands

### `wit init`
Initialize a new wit repository in the current directory. Creates a `.wit` directory to store version history.

**Usage:**
```bash
wit init
```

**Example output:**
```
Initialized empty .wit repository in C:\Users\user\Desktop\my_project
```

**Example output (if reinitializing):**
```
Reinitialized existing .wit repository
```

---

### `wit add <name>`
Add files or directories to the staging area. Use `"."` to add all files.

**Usage:**
```bash
wit add <file_or_directory>
wit add .
```

**Examples:**

Add a specific file:
```bash
wit add README.txt
```
Output:
```
Added README.txt to staging area
```

Add all files and directories:
```bash
wit add .
```
Output:
```
Added all files to staging area
```

Add a directory:
```bash
wit add src/
```
Output:
```
Added src to staging area
```

**Note:** Files listed in `.witignore.txt` will not be added to the staging area.

---

### `wit commit -m "message"`
Create a snapshot of the staged files with a commit message. Commits are identified by numeric IDs.

**Usage:**
```bash
wit commit -m "Your commit message"
```

**Example:**
```bash
wit commit -m "Initial commit with project files"
```
Output:
```
Committed with id 12345, message: Initial commit with project files
```

**Creating subsequent commits:**
```bash
wit add fileA.txt
wit commit -m "Update fileA.txt"
```
Output:
```
Committed with id 12346, message: Update fileA.txt
```

---

### `wit status`
Display the current status of your repository, showing:
- **Untracked files:** Files not yet added to staging
- **Changes not staged for commit:** Modified files not yet added to staging
- **Changes to be committed:** Files ready to be committed

**Usage:**
```bash
wit status
```

**Example output (clean working directory):**
```
nothing to commit, working tree clean
```

**Example output (with changes):**
```
Untracked files:
	new_file.txt

Changes not staged for commit:
	modified: README.md

Changes to be committed:
	new file: config.py
```

---

### `wit checkout <commit_id>`
Restore files from a specific commit. Updates both the working directory and staging area.

**Usage:**
```bash
wit checkout <commit_id>
```

**Example:**
```bash
wit checkout 12345
```
Output:
```
Now on commit:	12345	Initial commit with project files	2026-02-16 14:23:45.123456
```

---

## Complete Workflow Example

Here's a real-world example demonstrating a complete workflow:

### Step 1: Initialize Repository
```bash
C:\Users\user\Desktop\my_project> wit init
```
Output:
```
Initialized empty .wit repository in C:\Users\user\Desktop\my_project
```

### Step 2: Create and Add Files
```bash
C:\Users\user\Desktop\my_project> wit add .
```
Output:
```
Added all files to staging area
```

### Step 3: Create First Commit
```bash
C:\Users\user\Desktop\my_project> wit commit -m "Initial commit"
```
Output:
```
Committed with id 12345, message: Initial commit
```

### Step 4: Check Status
```bash
C:\Users\user\Desktop\my_project> wit status
```
Output:
```
nothing to commit, working tree clean
```

### Step 5: Modify a File and Check Status
```bash
C:\Users\user\Desktop\my_project> wit status
```
Output:
```
Changes not staged for commit:
	modified: README.txt
```

### Step 6: Stage and Commit Changes
```bash
C:\Users\user\Desktop\my_project> wit add README.txt
wit commit -m "Update README.txt with documentation"
```
Output:
```
Added README.txt to staging area
Committed with id 12346, message: Update README.txt with documentation
```

### Step 7: View and Switch Between Commits
```bash
C:\Users\user\Desktop\my_project> wit checkout 12345
```
Output:
```
Now on commit:	12345	Initial commit	2026-02-16 14:15:00.000000
```

---

## Advanced Features

### .witignore File
Create a `.witignore.txt` file in your project root to exclude files from version control. List one filename or directory per line.

**Example `.witignore.txt`:**
```
node_modules
.env
cache/
temp_files.txt
```

Files and directories listed here will not be tracked by wit.

### Commit History
Commit information is stored in `.wit/commits/commits_details.txt` with the following format:
```
COMMIT DETAILS: Id, Message, Time
12345	Initial commit	2026-02-16 14:15:00.123456
12346	Update README.txt	2026-02-16 14:20:15.654321
```

---

## Tips & Best Practices

1. **Commit Frequently:** Make small, focused commits with clear messages to maintain a useful history.
2. **Check Status Often:** Use `wit status` before committing to ensure you're tracking the right files.
3. **Use .witignore:** Exclude build artifacts, dependencies, and temporary files using `.witignore.txt`.
4. **Clear Commit Messages:** Write descriptive commit messages that explain what changed and why.

---

## Troubleshooting

### Error: ".wit directory does not exist"
Run `wit init` to initialize a repository in the current directory.

### Error: "Commit with id X does not exist"
The commit ID is invalid. Use the correct commit ID shown in your commit history.

### Error: "There are uncommitted changes"
You cannot checkout to a different commit while having staged changes. Commit your changes first or reset the staging area.

---

## Project Structure

```
.wit/
├── commits/
│   ├── 12345/          (First commit directory)
│   ├── 12346/          (Second commit directory)
│   └── commits_details.txt
└── stage/              (Staging area)
.witignore.txt         (Optional file list to ignore)
```

---

## License

This project is provided as-is for educational purposes.
