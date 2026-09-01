from pathlib import Path



IGNORED_DIRECTORIES = {".git",
                       ".venv",
                       "__pycache__",
                       ".pytest_cache"}


def list_files(repository_path:str)->list[str]:
    root= Path(repository_path)

    if not root.exists():
        raise FileNotFoundError
    (f"Repository path does not exist : {repository_path}")  


    if not root.is_dir():
        raise ValueError(f"Repository path must be a directory : {repository_path}")


    files :list[str] = []


    for path in root.rglob("*"):
        if not path.is_file():
            continue


        relative_path = path.relative_to(root)


        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        files.append(relative_path.as_posix())


    return sorted(files)    

        
            
def read_file(
    repository_path: str,
    file_path: str,
) -> str:
    root = Path(repository_path).resolve()
    target = (root / file_path).resolve()

    if not target.is_relative_to(root):
        raise ValueError("File must be inside the repository.")

    if not target.exists():
        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    if not target.is_file():
        raise ValueError(
            f"Path must be a file: {file_path}"
        )

    return target.read_text(encoding="utf-8")
        

def search_code(
    repository_path: str,
    query: str,
    max_results: int = 50,
) -> list[str]:
    matches: list[str] = []

    for file_path in list_files(repository_path):
        full_path = Path(repository_path) / file_path

        try:
            content = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):
            if query.lower() in line.lower():
                matches.append(
                    f"{file_path}:{line_number}: {line.strip()}"


    )

                if len(matches) >= max_results:
                 return matches

        

        return matches