import os
from fastapi import HTTPException
from pathlib import Path
from .config import settings

def secure_path(filename: str) -> Path:
    """
    Resolves a filename to a full path and ensures it stays within the DATA_DIR.
    Handles absolute paths, relative paths, and paths prefixed with '/data/'.
    """
    if not filename:
         raise HTTPException(status_code=400, detail="Filename cannot be empty.")

    # 1. Convert to Path object for initial checks
    path_obj = Path(filename)
    
    # 2. Check if it's a valid system absolute path
    if path_obj.is_absolute():
        try:
            resolved_path = path_obj.resolve()
            # If it's explicitly inside the DATA_DIR, it's valid. Return it.
            if str(resolved_path).startswith(str(settings.DATA_DIR.resolve())):
                return resolved_path
        except Exception:
            pass
        # If absolute but invalid, fall through to treat as relative

    # 3. Normalize: Treat as relative path
    # Remove leading slashes to turn "/data/file" into "data/file"
    clean_name = str(filename).replace("\\", "/").lstrip("/")
    
    # 4. Handle "data/" duplication
    if clean_name.startswith("data/"):
        clean_name = clean_name[5:] # Remove first 5 chars
    
    # 5. Resolve the full path
    full_path = (settings.DATA_DIR / clean_name).resolve()
    
    # 6. Final Security Check
    if not str(full_path).startswith(str(settings.DATA_DIR.resolve())):
        raise HTTPException(
            status_code=403, 
            detail=f"Security Alert: Access to {filename} is forbidden. You can only access files in /data."
        )
    
    return full_path