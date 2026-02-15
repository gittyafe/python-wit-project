import os
import shutil
from datetime import datetime

from helper_files import (found_in_witignore, copy_all_needed,
                         compare_paths, get_last_commit_id,
                         return_all_files_in_dir, remove_files_in_dir,
                         get_commit_line_by_id)


def status_def():
    """Display status of working directory."""
    if not os.path.exists(os.path.join(os.getcwd(), ".wit")):
        return ".wit directory does not exist"

    last_commit_id = get_last_commit_id()
    result = ""
    curr_path = os.getcwd()
    stage_path = os.path.join(curr_path, ".wit", "stage")
    commit_path = (os.path.join(curr_path, ".wit", "commits",
                                last_commit_id)
                   if last_commit_id else None)

    res_untracked = compare_paths(curr_path, stage_path, "untrucked")
    res_unstaged = compare_paths(curr_path, stage_path, "unstaged")
    res_uncommited = (compare_paths(stage_path, commit_path,
                                    "uncommited")
                      if commit_path
                      else return_all_files_in_dir(stage_path,
                                                   "new file: "))

    if res_untracked != "":
        result += "Untracked files:\n"
        result += res_untracked
    if res_unstaged != "":
        result += "Changes not staged for commit:\n"
        result += res_unstaged
    if res_uncommited != "":
        result += "Changes to be committed:\n"
        result += res_uncommited
    if result == "":
        result = "nothing to commit, working tree clean\n"

    return result


def add_def(name):
    """Add file/folder to staging area."""
    try:
        if (found_in_witignore(name) or name == ".wit" or
                name == ".witignore.txt"):
            return (f"'{name}' is ignored file and cannot be added to "
                    "staging area")

        if name == ".":
            stage_path = os.path.join(os.getcwd(), ".wit", "stage")
            shutil.rmtree(stage_path)
            os.mkdir(stage_path)
            copy_all_needed(os.getcwd(), stage_path)
            return "Added all files to staging area"

        stage_item_path = os.path.join(os.getcwd(), ".wit", "stage",
                                       name)
        shutil.rmtree(stage_item_path, ignore_errors=True)
        if os.path.isdir(os.path.join(os.getcwd(), name)):
            os.mkdir(stage_item_path)
            src_path = os.path.join(os.getcwd(), name)
            copy_all_needed(src_path, stage_item_path)
        else:
            shutil.copy2(os.path.join(os.getcwd(), name),
                          stage_item_path)

        return f"Added {name} to staging area"

    except Exception as e:
        return f"error: {str(e)}"


def init_def():
    """Initialize .wit repository."""
    flag_is_already = False
    wit_path = os.path.join(os.getcwd(), ".wit")
    if os.path.exists(wit_path):
        shutil.rmtree(wit_path)
        flag_is_already = True
    os.mkdir(wit_path)
    commits_path = os.path.join(wit_path, "commits")
    os.mkdir(commits_path)
    commits_details_path = os.path.join(commits_path,
                                        "commits_details.txt")
    with open(commits_details_path, "w") as f:
        f.write("COMMIT DETAILS: Id, Message, Time\n")
    os.mkdir(os.path.join(wit_path, "stage"))
    if flag_is_already:
        return "Reinitialized existing .wit repository"
    else:
        return f"Initialized empty .wit repository in {os.getcwd()}"

def commit_def(msg):
    """Create a commit with the staging area."""
    commit_id = get_last_commit_id()

    # Check if there is nothing to commit
    stage_path = os.path.join(os.getcwd(), ".wit", "stage")
    if os.path.exists(stage_path) and not os.listdir(stage_path):
        return "Nothing to commit"

    if commit_id and os.path.exists(os.path.join(os.getcwd(), ".wit",
                                                   "commits",
                                                   commit_id)):
        last_commit_path = os.path.join(os.getcwd(), ".wit", "commits",
                                        commit_id)
        res = compare_paths(stage_path, last_commit_path,
                            "uncommited")
        if res == "":
            return "Nothing to commit"

    if commit_id is None:  # First commit
        commit_id = "12345"
    else:
        commit_id = str(int(commit_id) + 1)

    curr_commit_path = os.path.join(os.getcwd(), ".wit", "commits",
                                     commit_id)
    os.mkdir(curr_commit_path)
    copy_all_needed(stage_path, curr_commit_path)
    commits_details_path = os.path.join(os.getcwd(), ".wit", "commits",
                                        "commits_details.txt")
    with open(commits_details_path, "a") as f:
        f.write(f"{commit_id}\t{msg}\t{datetime.now()}\n")
    return f"Committed with id {commit_id}, message: {msg}"


def checkout_def(commit_id):
    """Checkout a specific commit."""
    try:
        if get_commit_line_by_id(commit_id) is None:
            return f"Commit with id {commit_id} does not exist"

        commit_id_path = os.path.join(os.getcwd(), ".wit", "commits",
                                       commit_id)
        stage_path = os.path.join(os.getcwd(), ".wit", "stage")
        last_commit_id = get_last_commit_id()
        if last_commit_id:
            last_commit_path = os.path.join(os.getcwd(), ".wit",
                                            "commits",
                                            last_commit_id)
            if compare_paths(stage_path, last_commit_path,
                             "uncommited") != "":
                return ("There are uncommitted changes. Use 'status' "
                        "to see details.")

        # Remove all files in stage and current dir except .wit
        shutil.rmtree(stage_path, ignore_errors=True)
        os.mkdir(stage_path)
        remove_files_in_dir(os.getcwd())

        copy_all_needed(commit_id_path, os.getcwd())
        return f"Now on commit:\t{get_commit_line_by_id(commit_id)}"

    except Exception as e:
        return f"error: {str(e)}"
