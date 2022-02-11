from subprocess import run
from pathlib import Path
from typing import Union, Optional

def path_to_str(path:Path)->str:
    return str(path).replace("\\", "/")


def git_update_file(absolute_file_path: Union[str, Path], commit_message:Optional[str]=None, run_sh: bool = True, keep_sh: bool = False) -> None:

    """
    A function for git add, commit, and push a file. The absolute path is important as the directory information is
    used to find the repo to update.
    """

    # formatting paths
    if type(absolute_file_path) is str:
        absolute_file_path = Path(absolute_file_path)
    dir = absolute_file_path.parent
    file = absolute_file_path.parts[-1]
    shell_file = dir / 'git_cmd.sh'
    dir_str = path_to_str(dir)
    shell_file_str = path_to_str(shell_file)
    # format commit message
    if commit_message is None:
        commit_message = f"[automated git action] Created/updated file {shell_file_str}!"
    # processing shell scripts for git commands
    with open(shell_file, 'w') as f:
        f.write("pwd \n")
        f.write(f"cd {dir_str} \n")
        f.write("pwd \n")
        f.write("git status \n")
        f.write(f"git add {file} \n")
        f.write(f"git commit -m'{commit_message}' \n")
        f.write("git push \n")
        if not keep_sh:
            f.write(f"rm {shell_file_str}")
    # run git commands
    if run_sh:
        run(f"bash {shell_file_str}", shell=True)