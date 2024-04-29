from fastapi import HTTPException, status

template_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Template not found"
)

