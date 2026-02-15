import os
import shutil
from datetime import datetime


#check if a dir is in .witignore
def found_in_witignore(file_name):
    witignore_path=os.path.join(os.getcwd(),".witignore.txt")
    if os.path.exists(witignore_path):
        with open(witignore_path, 'r') as f:
            for line in f:
                if line.strip() == file_name:
                    return True
    return False


# copy all the files and folders from src to dest except the ones that are in the .witignore and the .wit and the .witignore.txt
def copy_all_needed(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            copysrc=root
            copydest=root.replace(src, dest)

            dirs[:] = [d for d in dirs if d != ".wit" and not found_in_witignore(d)]
            for d in dirs:
                os.mkdir(os.path.join(copydest, d))
            
            # Copy files
            for f in files:
                if not (f==".witignore.txt" or found_in_witignore(f)):
                    shutil.copy2(os.path.join(root, f), os.path.join(copydest, f))
    except Exception as e:
        return f"error: {str(e)}"
            


#gets 2 paths to compare and string that tells what to do with the diffs.
def compare_paths(src, dest,string):
    curr_path = os.getcwd()
    result=""
    for root, dirs, files in os.walk(src):#pass on all the files in the src and check if they are in the dest and if they are different or not and so on
        dirs[:] = [d for d in dirs if d != ".wit" and not found_in_witignore(d)] #remove the .wit and the files that are in the .witignore from the dirs list because we dont care about them
        files[:] = [f for f in files if f != ".witignore.txt" and not found_in_witignore(f)] #remove the .witignore.txt and the files that are in the .witignore from the files list because we dont care about them
        copysrc=root
        copydest=root.replace(src, dest)
        for f in files: #for the changes in the files that in the src - we will check if they are new or deleted or changed and print them according to the string
            if not os.path.exists(os.path.join(copydest,f)):
                if string == "unstaged":
                    continue #not go with the else
                elif string == "untrucked":
                    result += "\t"+f+"\n"
                else:
                    result += "\tnew file: "+f+"\n"

            elif is_diff_file(os.path.join(copysrc,f),os.path.join(copydest,f)):
                if string == "untrucked":
                    continue #not go with the else
                else:
                    result += "\tmodified: "+f+"\n"

        if os.path.exists(copydest) and not string == "untrucked": #if we are in the untrucked we dont care about the deleted files and folders because they are not in the stage or the commit so they are not untrucked
            for fd in os.listdir(copydest): #for the changes in the files and folders that in the dest but not in the src - we will return false or print them according to the string
                if not os.path.exists(os.path.join(copysrc,fd)):
                    if os.path.isfile(os.path.join(copydest,fd)):
                        result += "\tdeleted: "+fd+"\n"
  
    return result
        

# get all the files in the dir and return them with the string before them
def return_all_files_in_dir(dir_path, string):
    result = ""
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            result += "\t"+string+f+"\n"
    return result


# check if there is a difference between 2 files - if there is a difference return true else return false
def is_diff_file(file1, file2):
    if os.path.getsize(file1) != os.path.getsize(file2):
        return True

    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while True:
            b1 = f1.read(4096)
            b2 = f2.read(4096)
            if b1 != b2:
                return True
            if not b1:  # End of file
                break

    return False


# return the last commit id from the commits_details.txt file - if there is no commit yet return None
def get_last_commit_id():
    commits_details_path = os.path.join(os.getcwd(), ".wit", "commits", "commits_details.txt")
    with open(commits_details_path, 'r') as f:
        lines = f.readlines()
        if len(lines) <= 1:  # No commits yet
            return None
        last_commit_line = lines[-1].strip()
        last_commit_id = last_commit_line.split("\t")[0].strip()  # Assuming the format is "Id, Message, Time"
        return last_commit_id


# remove all the files and folders in the dir except the .wit and the .witignore.txt and the files that are in the .witignore
def remove_files_in_dir(dir_path):
    for fd in os.listdir(dir_path):
        if fd == ".wit" or fd == ".witignore.txt" or found_in_witignore(fd):
            continue
        fd_path = os.path.join(dir_path, fd)
        if os.path.isfile(fd_path):
            os.remove(fd_path)
        elif os.path.isdir(fd_path):
            shutil.rmtree(fd_path)


# return the line of the commit with the given id from the commits_details.txt file - if there is no commit with the given id return None
def get_commit_line_by_id(commit_id):
    with open(os.path.join(os.getcwd(), ".wit","commits", "commits_details.txt"), "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(commit_id):
                return line.strip()
