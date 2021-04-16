"""
Clone well-loved Python repositories and parse them to get variable names. 
"""
import multiprocessing
from clone_repo import clone_repo

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
    # From: https://stackoverflow.com/a/7207336/13697995
    proc = []
    # Start each process
    for repo in REPOS:
        p = multiprocessing.Process(target=clone_repo, args=(repo,))
        p.start()
        proc.append(p)
    # Wait on each process
    for p in proc:
        p.join()

# Parse all .py files in repos/ 
# Update a csv of variable names after parsing each file. HOW?!