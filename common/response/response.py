from rest_framework import status
from rest_framework.response import Response


class ErrorResponse:
    """
    공통 에러 응답 처리를 위한 헬퍼 클래스
    """
    @staticmethod
    def not_found(message: str, code: str = "not_found") -> Response:
        return Response(
            {"error": {"code": code, "message": message}},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def bad_request(message: str, code: str = "bad_request") -> Response:
        return Response(
            {"error": {"code": code, "message": message}},
            status=status.HTTP_400_BAD_REQUEST,
        )