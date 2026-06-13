import os

# Ignore junk/cache/IDE dirs
IGNORE_DIRS = {
    "build", "dist", "out", "bin", "obj", "target", "Debug", "Release",
    ".cache", ".gradle", ".cargo", ".venv", "env", 
    "CMakeFiles", "cmake-build-debug", "cmake-build-release",
    "coverage", "htmlcov", ".pytest_cache", ".tox", ".mypy_cache", ".ruff_cache",
    ".git", ".svn", ".hg", ".idea", ".vscode", ".vs", ".DS_Store",
    "__pycache__", "node_modules", "jspm_packages", "bower_components",
    ".nuget", "Packages", "Pods", "DerivedData", ".next", ".svelte-kit",
    ".angular", "typings", ".docusaurus", ".yarn", ".pnp",
    "vendor", "classes", "logs",
}

# Strong project markers
PROJECT_MARKERS = {
    ".cpp": ["CMakeLists.txt", "compile_commands.json"],
    ".py": ["pyproject.toml", "requirements.txt", "setup.py"],
    ".rs": ["Cargo.toml"],
    ".ts": ["tsconfig.json", "package.json"],
    ".js": ["package.json"],
    ".java": ["pom.xml", "build.gradle"],
    ".cs": [".csproj", ".sln"],
}




def getProjectRootsAndProjectDirs(base_path: str) -> dict:
    """Detect project roots in a folder tree"""
    project_roots = {}
    project_dirs = {}

    previous_project_root=None
    for root, dirs, files in os.walk(base_path):
        # --- Skip ignored dirs ---
        clean_dirs = []
        print("=============",files)
        for d in dirs:
            
            if d not in IGNORE_DIRS:
                clean_dirs.append(d)
        dirs[:] = clean_dirs  # replace dirs in-place so os.walk respects it

        # --- Check files in this folder ---
              
        #splited_root,splited_dir=os.path.split(root)

        if dirs:
            for dir in dirs:
                project_dirs[os.path.join(root,dir)]=root 
        
        """else:
            project_dirs[root]=None 
        """    

        files_set = set(files)
        for lang, markers in PROJECT_MARKERS.items():
            for marker in markers:
                #print(marker)
                if marker in files_set:
                    project_roots[root]=lang
                    #stop scanning deeper into this root
                    dirs.clear()
                    break
  
            if root in project_roots:    
                break
            """        
        if previous_project_root :
            print(previous_project_root,"--->>",root)"""
    return project_roots,project_dirs


if __name__ == "__main__":
    project_path = "/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock" 
    result,dirs = getProjectRootsAndProjectDirs(project_path)
    print(result)
    print("\n\n",dirs)
