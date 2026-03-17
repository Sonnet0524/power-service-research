#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版：将ASCII艺术转换为专业图片（只处理真正的ASCII图形）
"""

from PIL import Image, ImageDraw, ImageFont
import os
import re
from pathlib import Path

class ImprovedAsciiArtToImage:
    """改进版ASCII艺术转换器"""
    
    # 麦肯锡风格配色
    COLORS = {
        'primary': '#1B365D',      # 深蓝
        'secondary': '#8B4513',    # 深棕
        'tertiary': '#2E5A4C',     # 森林绿
        'accent': '#C9A227',       # 金色
        'light': '#F5F5F0',        # 米白
        'text': '#2C3E50',         # 文本色
        'white': '#FFFFFF',
        'bg_gray': '#FAFAFA',
    }
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.image_counter = 0
        
        # 加载字体
        self.font_paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
        ]
        self.font = self._load_font(22)
        self.font_small = self._load_font(16)
        self.font_title = self._load_font(26)
        self.font_mono = self._load_font(18)
        
    def _load_font(self, size):
        """加载字体"""
        for path in self.font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    pass
        return ImageFont.load_default()
    
    def is_valid_ascii_art(self, content):
        """检查是否为有效的ASCII艺术（包含图形字符）"""
        # 必须包含ASCII图形字符
        ascii_chars = set('┌─┐│└┘├┤┼┬┴┼═║╔╗╚╝╠╣╦╩╬─━┃┏┓┗┛┣┫┻┳')
        content_chars = set(content)
        
        # 如果没有ASCII图形字符，则不是ASCII艺术
        if not (content_chars & ascii_chars):
            return False
        
        # 如果只有方括号表单字段（如[手工录入]），则不是ASCII艺术
        if re.search(r'\[.*?\]', content) and not re.search(r'[┌─┐│└┘]', content):
            return False
        
        return True
    
    def generate_image(self, ascii_art, doc_name):
        """生成图片"""
        if not self.is_valid_ascii_art(ascii_art):
            return None
        
        self.image_counter += 1
        filename = f"{doc_name}_{self.image_counter:03d}.png"
        filepath = self.output_dir / filename
        
        # 分析ASCII艺术类型
        if '↓' in ascii_art or '→' in ascii_art or '│' in ascii_art:
            img = self._create_improved_flow_chart(ascii_art)
        elif '┌' in ascii_art and '┐' in ascii_art:
            img = self._create_improved_box_diagram(ascii_art)
        else:
            img = self._create_improved_text_card(ascii_art)
        
        if img:
            img.save(filepath, 'PNG', dpi=(300, 300))
            return str(filepath)
        return None
    
    def _create_improved_box_diagram(self, ascii_art):
        """创建改进的方框图"""
        lines = [l.rstrip() for l in ascii_art.strip().split('\n') if l.strip()]
        if not lines:
            return None
        
        # 计算尺寸
        max_chars = max(len(l) for l in lines)
        width = max(800, max_chars * 22 + 100)
        height = max(400, len(lines) * 32 + 80)
        
        img = Image.new('RGB', (width, height), self.COLORS['bg_gray'])
        draw = ImageDraw.Draw(img)
        
        # 绘制阴影
        shadow_offset = 4
        draw.rounded_rectangle(
            [30 + shadow_offset, 30 + shadow_offset, width-30 + shadow_offset, height-30 + shadow_offset],
            radius=12,
            fill='#E0E0E0'
        )
        
        # 绘制主背景
        draw.rounded_rectangle(
            [30, 30, width-30, height-30],
            radius=12,
            fill=self.COLORS['white'],
            outline=self.COLORS['primary'],
            width=3
        )
        
        # 绘制顶部装饰线
        draw.rounded_rectangle(
            [30, 30, width-30, 38],
            radius=4,
            fill=self.COLORS['accent']
        )
        
        # 绘制内容
        y = 60
        for line in lines:
            # 移除边框字符，保留内容
            content = re.sub(r'^[┌├│└┏┣┃]', '  ', line)
            content = re.sub(r'[─┬┼┴┯┷┿━]', '─', content)
            content = re.sub(r'[┐┤┘┓┫┛]', '  ', content)
            content = content.strip()
            
            if content and content not in ['', '─' * len(content)]:
                # 检测是否是标题（居中且特殊字符）
                if '驻点' in content or '体系' in content or '工作' in content:
                    draw.text((50, y), content, font=self.font_title, fill=self.COLORS['primary'])
                else:
                    draw.text((50, y), content, font=self.font, fill=self.COLORS['text'])
            y += 30
        
        return img
    
    def _create_improved_flow_chart(self, ascii_art):
        """创建改进的流程图"""
        lines = [l.rstrip() for l in ascii_art.strip().split('\n') if l.strip()]
        
        # 解析流程步骤和箭头
        steps = []
        current_step = []
        
        for line in lines:
            if '↓' in line or '→' in line:
                if current_step:
                    steps.append('\n'.join(current_step))
                    current_step = []
            elif any(char in line for char in ['驻点', '服务', '信息', '资源', '准备', '走访', '回访']):
                current_step.append(line.strip())
        
        if current_step:
            steps.append('\n'.join(current_step))
        
        if not steps:
            return None
        
        # 创建图片
        width = 900
        box_height = 80
        box_width = 280
        spacing = 40
        height = max(500, len(steps) * (box_height + spacing) + 100)
        
        img = Image.new('RGB', (width, height), self.COLORS['bg_gray'])
        draw = ImageDraw.Draw(img)
        
        # 绘制步骤框
        colors = [self.COLORS['primary'], self.COLORS['tertiary'], self.COLORS['secondary']]
        
        for i, step in enumerate(steps):
            y = 60 + i * (box_height + spacing)
            color = colors[i % len(colors)]
            
            # 绘制阴影
            draw.rounded_rectangle(
                [(width - box_width)//2 + 4, y + 4, (width + box_width)//2 + 4, y + box_height + 4],
                radius=10,
                fill='#D0D0D0'
            )
            
            # 绘制步骤框
            draw.rounded_rectangle(
                [(width - box_width)//2, y, (width + box_width)//2, y + box_height],
                radius=10,
                fill=color,
                outline=self.COLORS['accent'],
                width=2
            )
            
            # 绘制文字（分行显示）
            step_lines = step.split('\n')
            line_height = 24
            start_y = y + (box_height - len(step_lines) * line_height) // 2
            
            for j, text in enumerate(step_lines):
                bbox = draw.textbbox((0, 0), text, font=self.font)
                text_width = bbox[2] - bbox[0]
                text_x = (width - text_width) // 2
                draw.text((text_x, start_y + j * line_height), text, 
                         font=self.font, fill=self.COLORS['white'])
            
            # 绘制向下箭头
            if i < len(steps) - 1:
                arrow_y = y + box_height + 8
                # 箭头三角形
                draw.polygon(
                    [(width//2, arrow_y + 25), (width//2 - 12, arrow_y + 5), (width//2 + 12, arrow_y + 5)],
                    fill=self.COLORS['accent']
                )
        
        return img
    
    def _create_improved_text_card(self, ascii_art):
        """创建改进的文本卡片"""
        lines = [l.rstrip() for l in ascii_art.strip().split('\n') if l.strip()]
        if not lines:
            return None
        
        width = 800
        height = max(300, len(lines) * 28 + 100)
        
        img = Image.new('RGB', (width, height), self.COLORS['bg_gray'])
        draw = ImageDraw.Draw(img)
        
        # 绘制卡片
        draw.rounded_rectangle(
            [40, 40, width-40, height-40],
            radius=15,
            fill=self.COLORS['white'],
            outline=self.COLORS['primary'],
            width=3
        )
        
        # 绘制顶部金色条
        draw.rounded_rectangle(
            [40, 40, width-40, 48],
            radius=4,
            fill=self.COLORS['accent']
        )
        
        # 绘制内容
        y = 70
        for line in lines:
            # 清理内容
            content = re.sub(r'^[┌├│└]', '  ', line)
            content = re.sub(r'[┐┤┘]$', '  ', content)
            content = content.strip()
            
            if content:
                draw.text((60, y), content, font=self.font, fill=self.COLORS['text'])
            y += 28
        
        return img


def main():
    """测试改进版转换器"""
    output_dir = Path('output/theory-images-v2')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    converter = ImprovedAsciiArtToImage(output_dir)
    
    # 测试示例
    test_arts = [
        """┌─────────────────────────────────────────────────────┐
│              武侯模式：流动式驻点                     │
│                                                     │
│  与长期驻扎不同，与景区季节性驻点相似                │
└─────────────────────────────────────────────────────┘""",
        
        """驻点前 ─── 信息准备（重点客户清单）
    ↓
驻点中 ─── 精准服务（针对性走访）
    ↓
驻点后 ─── 跟踪回访（确保问题解决）""",
    ]
    
    for i, art in enumerate(test_arts):
        result = converter.generate_image(art, "test")
        if result:
            print(f"✓ 生成图片: {result}")
        else:
            print(f"✗ 跳过无效的ASCII艺术")


if __name__ == '__main__':
    main()
