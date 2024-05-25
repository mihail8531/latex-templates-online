from fastapi import HTTPException

tickets_set_not_found = HTTPException(status_code=404, detail="Tickets set not found")
