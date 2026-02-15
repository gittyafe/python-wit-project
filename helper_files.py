import os
import shutil


def found_in_witignore(file_name):
    """Check if a dir/file is in .witignore."""
    witignore_path = os.path.join(os.getcwd(), ".witignore.txt")
    if os.path.exists(witignore_path):
        with open(witignore_path, 'r') as f:
            for line in f:
                if line.strip() == file_name:
                    return True
    return False


def copy_all_needed(src, dest):
    """Copy all files/folders from src to dest.

    Excludes .wit, .witignore.txt, and files in .witignore.
    """
    import os
    import shutil


def found_in_witignore(file_name):
    """Check if a dir/file is in .witignore."""
    witignore_path = os.path.join(os.getcwd(), ".witignore.txt")
    if os.path.exists(witignore_path):
        with open(witignore_path, "r") as f:
            for line in f:
                if line.strip() == file_name:
                    return True
    return False


def copy_all_needed(src, dest):
    """Copy all files/folders from src to dest.

    Excludes .wit, .witignore.txt, and files in .witignore.
    """
    try:
        for root, dirs, files in os.walk(src):
            copysrc = root
            copydest = root.replace(src, dest)

            dirs[:] = [d for d in dirs if d != ".wit" and
                        not found_in_witignore(d)]
            for d in dirs:
                os.mkdir(os.path.join(copydest, d))

            # Copy files
            for f in files:
                if f != ".witignore.txt" and not found_in_witignore(f):
                    shutil.copy2(os.path.join(root, f),
                                    os.path.join(copydest, f))
    except Exception as e:
        return f"error: {str(e)}"


def compare_paths(src, dest, string):
    """Compare two paths and identify differences.

    Args:
        src: Source path to compare.
        dest: Destination path to compare.
        string: Type of comparison ('unstaged', 'untracked', 'uncommited').

    Returns:
        String with formatted differences.
    """
    curr_path = os.getcwd()
    result = ""
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d != ".wit" and
                    not found_in_witignore(d)]
        files[:] = [f for f in files if f != ".witignore.txt" and
                    not found_in_witignore(f)]
        copysrc = root
        copydest = root.replace(src, dest)
        for f in files:
            if not os.path.exists(os.path.join(copydest, f)):
                if string == "unstaged":
                    continue
                elif string == "untrucked":
                    result += f"\t{f}\n"
                else:
                    result += f"\tnew file: {f}\n"

            elif is_diff_file(os.path.join(copysrc, f),
                                os.path.join(copydest, f)):
                if string == "untrucked":
                    continue
                else:
                    result += f"\tmodified: {f}\n"

        if os.path.exists(copydest) and string != "untrucked":
            for fd in os.listdir(copydest):
                if not os.path.exists(os.path.join(copysrc, fd)):
                    if os.path.isfile(os.path.join(copydest, fd)):
                        result += f"\tdeleted: {fd}\n"

    return result


def return_all_files_in_dir(dir_path, string):
    """Get all files in dir and return with string prefix."""
    result = ""
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            result += f"\t{string}{f}\n"
    return result


def is_diff_file(file1, file2):
    """Check if there is a difference between 2 files.

    Returns:
        True if files differ, False otherwise.
    """
    if os.path.getsize(file1) != os.path.getsize(file2):
        return True

    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        while True:
            b1 = f1.read(4096)
            b2 = f2.read(4096)
            if b1 != b2:
                return True
            if not b1:  # End of file
                break

    return False


def get_last_commit_id():
    """Return the last commit id from commits_details.txt.

    Returns:
        Last commit id or None if no commits yet.
    """
    commits_details_path = os.path.join(
        os.getcwd(), ".wit", "commits", "commits_details.txt")
    with open(commits_details_path, "r") as f:
        lines = f.readlines()
        if len(lines) <= 1:  # No commits yet
            return None
        last_commit_line = lines[-1].strip()
        last_commit_id = last_commit_line.split("\t")[0].strip()
        return last_commit_id


def remove_files_in_dir(dir_path):
    """Remove all files/folders except .wit, .witignore.txt, ignored."""
    for fd in os.listdir(dir_path):
        if fd == ".wit" or fd == ".witignore.txt" or found_in_witignore(fd):
            continue
        fd_path = os.path.join(dir_path, fd)
        if os.path.isfile(fd_path):
            os.remove(fd_path)
        elif os.path.isdir(fd_path):
            shutil.rmtree(fd_path)


def get_commit_line_by_id(commit_id):
    """Get the commit line with given id from commits_details.txt.

    Returns:
        Commit line or None if no commit with given id.
    """
    commits_details_path = os.path.join(
        os.getcwd(), ".wit", "commits", "commits_details.txt")
    with open(commits_details_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(commit_id):
                return line.strip()
    return None
