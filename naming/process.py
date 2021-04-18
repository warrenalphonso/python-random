"""
Parallelize cloning, and parsing Python files to extract names. 
"""
from collections import Counter
from multiprocessing import Pool
from os import walk, path
from pathlib import Path
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
    # If stats.pkl already exists, just update it
    if Path("stats.pkl").exists():
        stats = pickle.load(open("stats.pkl", "rb"))
    else:
        stats = {}

    # Create pool of max number of workers
    pool = Pool()

    # Clone each repo
    pool.map(clone_repo, REPOS)
    pool.close()
    pool.join()

    # Parse all files in repos/
    for repo in REPOS:
        if repo in stats:
            continue

        stats[repo] = {
            "variables": Counter(),
            "functions": Counter(),
            "imports": Counter(),
            "paths": [],
            "files": 0
        }

        print(f"Started parsing {repo}.")
        pool = Pool()
        # Iterate through all .py files
        for dirpath, _, files in walk(f"repos/{repo}"):
            py_files = (path.join(dirpath, file)
                        for file in files if file.endswith(".py"))
            for variables, functions, imports, filename in pool.map(parse_file, py_files):
                stats[repo]["variables"] += Counter(variables)
                stats[repo]["functions"] += Counter(functions)
                stats[repo]["imports"] += Counter(imports)
                stats[repo]["paths"].append(filename)
                stats[repo]["files"] += 1
        #! Make sure to wait before changing repo
        pool.close()
        pool.join()

        print(f"Finished parsing {repo}.")

    # Save
    pickle.dump(stats, open("stats.pkl", "wb"))
