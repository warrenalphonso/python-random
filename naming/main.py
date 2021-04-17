"""
Clone well-loved Python repositories and parse them to get variable names. 
"""
from collections import Counter
import multiprocessing
from os import walk, path
import pickle
from clone_repo import clone_repo
from parse_file import parse_file

# List from:
# https://dev.to/biplov/17-popular-python-opensource-projects-on-github-21ae
REPOS = [
    "tensorflow/tensorflow",
    "ytdl-org/youtube-dl",
    "nvbn/thefuck",
    "pallets/flask",
    "django/django",
    "keras-team/keras",
    "httpie/httpie",
    "ansible/ansible",
    "psf/requests",
    "scikit-learn/scikit-learn",
    "pytorch/pytorch",
    "scrapy/scrapy",
    "ageitgey/face_recognition",
    "pandas-dev/pandas",
    "getsentry/sentry",
    "pypa/pipenv",
    "fastai/fastai"
]


# def parse_dir(repo_stats, repo: str, dirpath, files):
#     """Each process can parse a directory."""
#     dir_stats = {
#         "variables": Counter(),
#         "functions": Counter(),
#         "imports": Counter(),
#         "files": 0
#     }

#     for name in files:
#         if name.endswith(".py"):
#             # Get full path
#             file_path = path.join(dirpath, name)
#             variables, functions, imports = parse_file(file_path)
#             dir_stats["variables"] += Counter(variables)
#             dir_stats["functions"] += Counter(functions)
#             dir_stats["imports"] += Counter(imports)
#             dir_stats["files"] += 1

#     repo_stats[repo]["variables"] += dir_stats["variables"]
#     repo_stats[repo]["functions"] += dir_stats["functions"]
#     repo_stats[repo]["imports"] += dir_stats["imports"]
#     repo_stats[repo]["files"] += dir_stats["files"]


if __name__ == "__main__":
    # repo_stats = multiprocessing.Manager().dict({repo: {
    repo_stats = {repo: {
        "variables": Counter(),
        "functions": Counter(),
        "imports": Counter(),
        "files": 0
    } for repo in REPOS}

    # From: https://stackoverflow.com/a/7207336/13697995
    proc = []
    # Start each process
    for repo in REPOS:
        p = multiprocessing.Process(target=clone_repo, args=(repo,))
        p.start()
        proc.append(p)
    # Wait on each process
    while proc:
        proc.pop().join()

    # Parse all .py files in repos/
    for repo in REPOS:
        print(f"Started parsing {repo}.")
        # Iterate through all .py files
        for dirpath, _, files in walk(f"repos/{repo}"):
            for name in files:
                if name.endswith(".py"):
                    # Get full path
                    file_path = path.join(dirpath, name)
                    variables, functions, imports = parse_file(file_path)
                    repo_stats[repo]["variables"] += Counter(variables)
                    repo_stats[repo]["functions"] += Counter(functions)
                    repo_stats[repo]["imports"] += Counter(imports)
                    repo_stats[repo]["files"] += 1

            # p = multiprocessing.Process(
            #     target=parse_dir, args=(repo_stats, repo, dirpath, files))
            # p.start()
            # proc.append(p)
        # # Wait on each process
        # while proc:
        #     proc.pop().join()

        print(f"Finished parsing {repo}.")

    # Save
    pickle.dump(repo_stats, open("repo_stats.pkl", "wb"))
