import openai
import base64
from PIL import Image
import io


class DiagnosticService:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def diagnose_rice_condition(self, image_path_or_bytes):
        if isinstance(image_path_or_bytes, str):
            with open(image_path_or_bytes, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        else:
            base64_image = base64.b64encode(image_path_or_bytes).decode("utf-8")

        prompt = """
        Bạn là một chuyên gia nông nghiệp chuyên về cây lúa. Hãy phân tích hình ảnh này và đưa ra một báo cáo chuẩn đoán chi tiết bao gồm:

        1. **Tình trạng tổng quan**: Mô tả tình trạng chung của cây lúa
        2. **Các bệnh phát hiện**: Nếu có, liệt kê các bệnh và mức độ nghiêm trọng
        3. **Nguyên nhân có thể**: Phân tích nguyên nhân gây bệnh
        4. **Khuyến nghị điều trị**: Các biện pháp điều trị cụ thể
        5. **Biện pháp phòng ngừa**: Cách phòng ngừa trong tương lai
        6. **Thời gian theo dõi**: Khi nào nên kiểm tra lại

        Trả lời bằng tiếng Việt, chi tiết và dễ hiểu cho nông dân.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",  # Hoặc gpt-4-vision-preview
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=1500,
            temperature=0.3,
        )

        return response.choices[0].message.content
