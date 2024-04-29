from fastapi import HTTPException, status

workspace_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found"
)

operation_not_permitted = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted"
)

user_not_in_workspace = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User not in workspace"
)

user_already_in_workspace = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already in workspace"
)
