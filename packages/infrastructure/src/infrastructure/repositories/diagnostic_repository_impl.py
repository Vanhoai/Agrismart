from google import genai
from google.genai import types

from core.configuration import Configuration
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.repositories import DiagnosticRepository


class DiagnosticRepositoryImpl(DiagnosticRepository):
    def __init__(self, configuration: Configuration) -> None:
        self.genai = genai.Client(api_key=configuration.GEMINI_API_KEY)

    async def diagnose_rice_condition(self, image: bytes) -> str:
        prompt = """
        Phân tích hình ảnh cây lúa này và tạo một báo cáo chuẩn đoán nông nghiệp chi tiết:
        
        ## TÌNH TRẠNG CÂY LÚA
        - Đánh giá tình trạng tổng quan
        - Giai đoạn sinh trưởng hiện tại
        
        ## CHẨN ĐOÁN BỆNH HẠI
        - Các bệnh/sâu hại phát hiện được
        - Mức độ nghiêm trọng (nhẹ/trung bình/nặng)
        
        ## NGUYÊN NHÂN & GIẢI PHÁP
        - Nguyên nhân có thể gây ra tình trạng này
        - Biện pháp điều trị cụ thể
        - Thuốc/phân bón khuyến nghị
        
        ## KHUYẾN CÁO
        - Biện pháp phòng ngừa
        - Lịch chăm sóc tiếp theo
        
        Viết bằng tiếng Việt, phong cách chuyên nghiệp nhưng dễ hiểu.
        """

        response = self.genai.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=image,
                    mime_type="image/jpeg",
                ),
                prompt,
            ],
        )

        message = response.text
        if message is None:
            raise ExceptionHandler(
                code=ErrorCodes.BAD_REQUEST,
                msg="Cannot generate diagnostic report 🙁",
            )

        return message
