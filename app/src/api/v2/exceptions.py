from fastapi import HTTPException, status


def handle_exception(exc: Exception) -> HTTPException:
    match exc:
        case FileNotFoundError():
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ресурс не найден"
            )
        case PermissionError():
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Отсутствует доступ"
            )
        case FileExistsError():
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Файл с таким именем уже существует"
            )
        case HTTPException():
            raise exc
        case _:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла внутренняя ошибка сервера"
            )
