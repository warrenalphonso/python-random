"""
Parallelize cloning, and parsing Python files to extract names. 
"""
from collections import Counter
from multiprocessing import Pool
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

if __name__ == "__main__":
    stats = {repo: {
        "variables": Counter(),
        "functions": Counter(),
        "imports": Counter(),
        "files": 0
    } for repo in REPOS}

    # Create pool of max number of workers
    pool = Pool()

    # Clone each repo
    pool.map(clone_repo, REPOS)

    # Parse all files in repos/
    for repo in REPOS:
        print(f"Started parsing {repo}.")
        # Iterate through all .py files
        for dirpath, _, files in walk(f"repos/{repo}"):
            py_files = (path.join(dirpath, file)
                        for file in files if file.endswith(".py"))
            for variables, functions, imports in pool.map(parse_file, py_files):
                stats[repo]["variables"] += Counter(variables)
                stats[repo]["functions"] += Counter(functions)
                stats[repo]["imports"] += Counter(imports)
                stats[repo]["files"] += 1

    print(f"Finished parsing {repo}.")

    # Save
    pickle.dump(stats, open("stats.pkl", "wb"))
