from pathlib import Path
from git import Repo, RemoteProgress


class CloneProgress(RemoteProgress):
    """Print progress, from: https://stackoverflow.com/a/53999435/13697995"""

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def update(self, op_code, cur_count, max_count=None, message=""):
        if message:
            print(f"{self.repo}: {message}")


def clone_repo(repo: str):
    directory = f"repos/{repo}"
    # Create a directory repos/ if it doesn't already exist
    if not Path(directory).exists():
        Path(directory).mkdir(parents=True, exist_ok=True)

        print(f"Cloning {repo}.")
        Repo.clone_from(
            f"https://github.com/{repo}", directory, progress=CloneProgress(repo))
        print(f"Finished cloning {repo}.")
