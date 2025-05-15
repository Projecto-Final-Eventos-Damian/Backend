from fastapi import Depends, HTTPException, status
from app.auth.auth_bearer import JWTBearer

def RoleChecker(allowed_roles: list[str]):
    if not allowed_roles:
            raise ValueError("RoleChecker: Se debe especificar al menos un rol")

    def checker(payload: dict = Depends(JWTBearer())):
        user_role = payload.get("role")
        if not user_role:
            raise HTTPException(status_code=401, detail="No se encontró rol en el token")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes"
            )
        return payload

    return checker
