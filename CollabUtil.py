import os

def get_path(view):
    path = view.file_name()
    if path == None:
        return '[No Name]'

    path = os.path.normpath(view.file_name())
    for project_path in view.window().folders():
        project_path = os.path.normpath(project_path)
        project_dir = os.path.basename(project_path)
        if path.startswith(project_path):
            path = path.replace(project_path, project_dir)

    return path
