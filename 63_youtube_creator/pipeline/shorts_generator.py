import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_shorts_pptx(output_path):
    prs = Presentation()
    
    # 쇼츠 9:16 비율 설정 (1080x1920 기준)
    # 1인치 = 914400 EMU. 9인치 x 16인치로 설정
    prs.slide_width = Inches(9)
    prs.slide_height = Inches(16)
    
    blank_slide_layout = prs.slide_layouts[6] # 빈 슬라이드 템플릿
    
    bg_color = RGBColor(0x12, 0x12, 0x12) # 다크모드 #121212
    cyan_color = RGBColor(0x00, 0xF0, 0xFF) # 시안 #00F0FF
    green_color = RGBColor(0x39, 0xFF, 0x14) # 그린 #39FF14
    white_color = RGBColor(0xFF, 0xFF, 0xFF)
    
    def add_dark_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color

    def create_text_box(slide, left, top, width, height):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        return tf

    def add_run(p, text, color, font_size, bold=False):
        run = p.add_run()
        run.text = text
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.bold = bold
        return run

    # --- Slide 1: 타이틀 ---
    slide1 = prs.slides.add_slide(blank_slide_layout)
    add_dark_background(slide1)
    
    tf1 = create_text_box(slide1, Inches(0.5), Inches(6), Inches(8), Inches(4))
    p1 = tf1.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    add_run(p1, "🎯 CRISP-DM?\n", cyan_color, 70, bold=True)
    add_run(p1, "데이터분석의 표준 6단계!", white_color, 45, bold=True)

    # --- Slide 2: 핵심 소개 ---
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_dark_background(slide2)
    tf2 = create_text_box(slide2, Inches(1), Inches(5), Inches(7), Inches(6))
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    add_run(p2, "데이터를 분석하려면?\n막 시작하면 안 된다.\n정해진 순서가 있어.\n\n", white_color, 40)
    add_run(p2, "그게 바로 CRISP-DM!\n", cyan_color, 50, bold=True)
    add_run(p2, "업계 표준 방법론이야.", white_color, 40)

    # --- Slide 3: 6단계 설명 ---
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_dark_background(slide3)
    # 텍스트 박스 시작 높이를 위로 올리고 세로 길이를 늘림
    tf3 = create_text_box(slide3, Inches(0.5), Inches(1.5), Inches(8), Inches(13))
    p3 = tf3.paragraphs[0]
    add_run(p3, "CRISP-DM 6단계\n", cyan_color, 60, bold=True)
    
    steps = [
        ("Step 1", "Business Understanding", "비즈니스 목표 정의"),
        ("Step 2", "Data Understanding", "데이터 수집 및 탐색"),
        ("Step 3", "Data Preparation", "데이터 정제 및 전처리"),
        ("Step 4", "Modeling", "알고리즘 학습 및 튜닝"),
        ("Step 5", "Evaluation", "성능 검증"),
        ("Step 6", "Deployment", "운영 환경 적용")
    ]
    
    for s_num, s_eng, s_kor in steps:
        p = tf3.add_paragraph()
        # 단락 간격 조절을 위해 불필요한 \n 제거, 폰트 사이즈 조정
        add_run(p, f"{s_num} ", cyan_color, 32, bold=True)
        add_run(p, f"{s_eng}", white_color, 32, bold=True)
        p_sub = tf3.add_paragraph()
        add_run(p_sub, f"  → {s_kor}", green_color, 28)

    # --- Slide 4: 우리 사례 ---
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_dark_background(slide4)
    tf4 = create_text_box(slide4, Inches(0.5), Inches(5), Inches(8), Inches(6))
    p4 = tf4.paragraphs[0]
    p4.alignment = PP_ALIGN.CENTER
    add_run(p4, "우리 3AI는?\n이 6단계를 완벽하게 적용 중!\n\n", cyan_color, 45, bold=True)
    
    p4_1 = tf4.add_paragraph()
    p4_1.alignment = PP_ALIGN.CENTER
    add_run(p4_1, "n8n 워크플로우 설계 = CRISP-DM 그 자체\n", white_color, 35)
    
    p4_2 = tf4.add_paragraph()
    p4_2.alignment = PP_ALIGN.CENTER
    add_run(p4_2, "Improve_stock 주식 분석 = EDA 교과서 흐름\n\n", white_color, 35)
    
    p4_3 = tf4.add_paragraph()
    p4_3.alignment = PP_ALIGN.CENTER
    add_run(p4_3, "수집 → 전처리 → 모델 → 신호생성 → 배포\n", green_color, 32, bold=True)
    add_run(p4_3, "= CRISP-DM 완벽 실행!", cyan_color, 40, bold=True)

    # --- Slide 5: 엔딩 ---
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_dark_background(slide5)
    tf5 = create_text_box(slide5, Inches(1), Inches(6), Inches(7), Inches(4))
    p5 = tf5.paragraphs[0]
    p5.alignment = PP_ALIGN.CENTER
    add_run(p5, "CRISP-DM은?\n무조건 알아야 할\n데이터 분석 기초!\n\n", white_color, 50, bold=True)
    add_run(p5, "구독 & 좋아요 🤍", green_color, 45, bold=True)

    # 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"✅ PPTX 생성 완료: {output_path}")

if __name__ == "__main__":
    out_file = r"D:\AI\63_youtube_creator\pipeline\output\crisp_dm_shorts.pptx"
    create_shorts_pptx(out_file)
