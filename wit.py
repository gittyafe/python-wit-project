import os
import shutil
from datetime import datetime
from helper_files import found_in_witignore, copy_all_needed, compare_paths, get_last_commit_id, return_all_files_in_dir, remove_files_in_dir, get_commit_line_by_id


def status_def():
    if not os.path.exists(os.path.join(os.getcwd(), ".wit")):
        return "error: .wit directory does not exist"

    last_commit_id = get_last_commit_id()
    result=""
    curr_path = os.getcwd()
    stage_path = os.path.join(curr_path,".wit","stage")
    commit_path = os.path.join(curr_path,".wit", "commits", last_commit_id) if last_commit_id else None #return the path only if there was a commit already - if not we will return None and the compare_paths will return "" because of the if condition in the status function
    
    res_untracked = compare_paths(curr_path, stage_path, "untrucked") #return the untrucked files
    res_unstaged = compare_paths(curr_path, stage_path, "unstaged") #return the changes that are in the curr but not in the stage
    res_uncommited = compare_paths(stage_path, commit_path, "uncommited") if commit_path else return_all_files_in_dir(stage_path, "new file: ") # return the changes that are in the stage but not in the commit - if there was a commit already. if not we will return all the files in the stage as new files because they are not commited yet and there is no commit to compare to.
    
    if(res_untracked != ""):
        result += "Untracked files:\n"
        result += res_untracked
    if(res_unstaged != ""):
        result += "Changes not staged for commit:\n"
        result += res_unstaged
    if(res_uncommited != ""):
        result += "Changes to be committed:\n"
        result += res_uncommited
    if result == "":
        result = "nothing to commit, working tree clean\n"

    return result


def add_def(name):
    try:
        if found_in_witignore(name) or name==".wit" or name==".witignore.txt":
            return f"'{name}' is ignored file and cannot be added to staging area"
        
        if name==".":
            shutil.rmtree(os.path.join(os.getcwd(), ".wit", "stage"))
            os.mkdir(os.path.join(os.getcwd(), ".wit", "stage"))
            copy_all_needed(os.path.join(os.getcwd()), os.path.join(os.getcwd(), ".wit", "stage"))
            return "Added all files to staging area"

        shutil.rmtree(os.path.join(os.getcwd(), ".wit", "stage", name), ignore_errors=True) #in case there is a file with the same name in the stage we will remove it before copying the new one
        if os.path.isdir(os.path.join(os.getcwd(), name)):
            os.mkdir(os.path.join(os.getcwd(), ".wit", "stage", name))    
            copy_all_needed(os.path.join(os.getcwd(),name), os.path.join(os.getcwd(), ".wit", "stage", name))
        else:
            shutil.copy2(os.path.join(os.getcwd(), name), os.path.join(os.getcwd(), ".wit", "stage", name))
        
        return f"Added {name} to staging area"

    except Exception as e:
        return f"error: {str(e)}"


def init_def():
    flag_is_already=False
    if os.path.exists(os.path.join(os.getcwd(), ".wit")):
        shutil.rmtree(os.path.join(os.getcwd(), ".wit"))
        flag_is_already=True
    os.mkdir(os.path.join(os.getcwd(), ".wit"))
    os.mkdir(os.path.join(os.getcwd(), ".wit", "commits"))
    with open(os.path.join(os.getcwd(), ".wit","commits", "commits_details.txt"), "w") as f:
        f.write("COMMIT DETAILS: Id, Message, Time\n")
    os.mkdir(os.path.join(os.getcwd(), ".wit", "stage"))
    if flag_is_already:
        return "Reinitialized existing .wit repository"
    else:
        return "Initialized empty .wit repository in "+os.getcwd()

def commit_def(msg):
    commit_id = get_last_commit_id()

    #if there is nothing to commit - return "Nothing to commit"
    if os.path.exists(os.path.join(os.getcwd(), ".wit", "stage")) and not os.listdir(os.path.join(os.getcwd(), ".wit", "stage")):
        return "Nothing to commit"
    if get_last_commit_id() and os.path.exists(os.path.join(os.getcwd(), ".wit", "commits", get_last_commit_id())):
        res = compare_paths(os.path.join(os.getcwd(), ".wit", "stage"), os.path.join(os.getcwd(), ".wit", "commits", get_last_commit_id()), "uncommited")
        if res == "":
            return "Nothing to commit"

    if  commit_id is None: # if it is the first commit
        commit_id = "12345"
    else:
        commit_id = str(int(commit_id) + 1)

    curr_commit_path = os.path.join(os.getcwd(),".wit","commits",commit_id)
    os.mkdir(curr_commit_path)
    copy_all_needed(os.path.join(os.getcwd(), ".wit", "stage"), curr_commit_path)
    with open(os.path.join(os.getcwd(), ".wit","commits", "commits_details.txt"), "a") as f:
        f.write(f"{commit_id}\t{msg}\t{datetime.now()}\n")
    return f"Committed with id {commit_id}, message: {msg}"


def checkout_def(commit_id):
    try:
        if get_commit_line_by_id(commit_id) is None:
            return f"Commit with id {commit_id} does not exist"

        commit_id_path = os.path.join(os.getcwd(), ".wit", "commits", commit_id)
        if compare_paths(os.path.join(os.getcwd(),".wit","stage"),os.path.join(os.getcwd(), ".wit", "commits", get_last_commit_id()), "uncommited") != "":
            return "There are uncommitted changes. Use 'status' to see details."
        
        # we want to remove all the files in the stage and in the curr dir except the .wit and the .witignore
        shutil.rmtree(os.path.join(os.getcwd(), ".wit", "stage"), ignore_errors=True)
        os.mkdir(os.path.join(os.getcwd(), ".wit", "stage"))
        remove_files_in_dir(os.getcwd())

        copy_all_needed(commit_id_path, os.path.join(os.getcwd()))        
        return f"Now on commit:\t{get_commit_line_by_id(commit_id)}"

    except Exception as e:
        return f"error: {str(e)}"


# print(init())
# print(add("."))
# print(commit("first commit"))
# print(status())
# print(checkout("12341"))
