import os


# feels like this should involve a context-manager somehow
def nuke(path):
    """Clean-up some test DB."""
    if os.path.exists(path):
        os.remove(path)
