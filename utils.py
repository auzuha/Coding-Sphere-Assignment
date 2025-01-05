from fastapi import HTTPException, status, Depends
from schemas import TokenData
from auth import decode_token
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()

def get_current_user(token: str = Depends(bearer_scheme)) -> TokenData:
    token_data = decode_token(token.credentials)
    return token_data

def role_required(required_role: str):
    def role_check(current_user: TokenData = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have {required_role} role",
            )
    return role_check
