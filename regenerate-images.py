#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成所有理论文档的ASCII艺术图片（改进版）
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image, ImageDraw, ImageFont
import os
import re
import shutil
from pathlib import Path

class OptimizedAsciiConverter:
    """优化的ASCII艺术转换器"""
    
    COLORS = {
        'primary': '#1B365D',
        'secondary': '#8B4513', 
        'tertiary': '#2E5A4C',
        'accent': '#C9A227',
        'light': '#F8F8F6',
        'text': '#2C3E50',
        'white': '#FFFFFF',
        'shadow': '#D0D0D0',
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
        self.font = self._load_font(24)
        self.font_small = self._load_font(18)
        self.font_title = self._load_font(28)
        
    def _load_font(self, size):
        for path in self.font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    pass
        return ImageFont.load_default()
    
    def is_valid_ascii_art(self, content):
        """检查是否为有效的ASCII艺术"""
        ascii_chars = set('┌─┐│└┘├┤┼┬┴┼═║╔╗╚╝╠╣╦╩╬─━┃┏┓┗┛┣┫┻┳↓→')
        content_chars = set(content)
        
        # 必须包含ASCII图形字符或流程箭头
        if not (content_chars & ascii_chars):
            return False
        
        # 过滤掉只有方括号的表单
        if content.count('[') > 3 and content.count('┌') == 0:
            return False
            
        return True
    
    def generate_image(self, ascii_art, doc_name):
        """生成图片"""
        if not self.is_valid_ascii_art(ascii_art):
            return None
        
        self.image_counter += 1
        filename = f"{doc_name}_{self.image_counter:03d}.png"
        filepath = self.output_dir / filename
        
        # 根据内容类型选择渲染方式
        if '↓' in ascii_art or ('→' in ascii_art and '│' in ascii_art):
            img = self._create_flow_diagram(ascii_art)
        elif '┌' in ascii_art or '╔' in ascii_art:
            img = self._create_architecture_diagram(ascii_art)
        else:
            img = self._create_text_visualization(ascii_art)
        
        if img:
            img.save(filepath, 'PNG', dpi=(300, 300))
            return str(filepath)
        return None
    
    def _create_flow_diagram(self, ascii_art):
        """创建流程图"""
        lines = [l.rstrip() for l in ascii_art.strip().split('\n') if l.strip()]
        
        # 提取步骤
        steps = []
        for line in lines:
            if '↓' not in line and '→' not in line:
                content = line.strip('├┤│─ ').strip()
                if content and len(content) > 3:
                    steps.append(content)
        
        if len(steps) < 2:
            return None
        
        # 计算尺寸
        width = 1000
        box_width = 350
        box_height = 90
        spacing = 50
        height = max(600, len(steps) * (box_height + spacing) + 150)
        
        img = Image.new('RGB', (width, height), self.COLORS['light'])
        draw = ImageDraw.Draw(img)
        
        colors = [self.COLORS['primary'], self.COLORS['tertiary'], self.COLORS['secondary']]
        
        for i, step in enumerate(steps):
            y = 80 + i * (box_height + spacing)
            color = colors[i % len(colors)]
            
            # 阴影
            draw.rounded_rectangle(
                [(width - box_width)//2 + 5, y + 5, (width + box_width)//2 + 5, y + box_height + 5],
                radius=12,
                fill=self.COLORS['shadow']
            )
            
            # 主框
            draw.rounded_rectangle(
                [(width - box_width)//2, y, (width + box_width)//2, y + box_height],
                radius=12,
                fill=color,
                outline=self.COLORS['accent'],
                width=3
            )
            
            # 文字
            bbox = draw.textbbox((0, 0), step, font=self.font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) // 2
            text_y = y + (box_height - 24) // 2
            draw.text((text_x, text_y), step, font=self.font, fill=self.COLORS['white'])
            
            # 箭头
            if i < len(steps) - 1:
                arrow_y = y + box_height + 10
                draw.polygon(
                    [(width//2, arrow_y + 30), (width//2 - 14, arrow_y + 5), (width//2 + 14, arrow_y + 5)],
                    fill=self.COLORS['accent']
                )
        
        return img
    
    def _create_architecture_diagram(self, ascii_art):
        """创建架构图"""
        lines = [l for l in ascii_art.strip().split('\n')]
        
        # 计算尺寸
        max_len = max(len(l) for l in lines) if lines else 50
        width = max(900, max_len * 18 + 100)
        height = max(500, len(lines) * 35 + 100)
        
        img = Image.new('RGB', (width, height), self.COLORS['light'])
        draw = ImageDraw.Draw(img)
        
        # 绘制背景卡片
        margin = 40
        draw.rounded_rectangle(
            [margin, margin, width-margin, height-margin],
            radius=15,
            fill=self.COLORS['white'],
            outline=self.COLORS['primary'],
            width=3
        )
        
        # 顶部装饰条
        draw.rounded_rectangle(
            [margin, margin, width-margin, margin+10],
            radius=5,
            fill=self.COLORS['accent']
        )
        
        # 绘制内容
        y = margin + 40
        for line in lines:
            # 清理边框字符
            content = line
            content = re.sub(r'^[┌├│└┏┣┃]', '  ', content)
            content = re.sub(r'[┐┤┘┓┫┛]$', '  ', content)
            content = content.rstrip()
            
            if content.strip():
                # 检测标题（包含特殊关键词）
                if any(kw in content for kw in ['武侯', '驻点', '体系', '核心', '价值']):
                    draw.text((margin + 50, y), content.strip(), 
                             font=self.font_title, fill=self.COLORS['primary'])
                else:
                    draw.text((margin + 50, y), content.strip(), 
                             font=self.font, fill=self.COLORS['text'])
            y += 34
        
        return img
    
    def _create_text_visualization(self, ascii_art):
        """创建文本可视化"""
        lines = [l.rstrip() for l in ascii_art.strip().split('\n') if l.strip()]
        if not lines:
            return None
        
        width = 900
        height = max(400, len(lines) * 32 + 100)
        
        img = Image.new('RGB', (width, height), self.COLORS['light'])
        draw = ImageDraw.Draw(img)
        
        # 卡片
        draw.rounded_rectangle(
            [50, 50, width-50, height-50],
            radius=15,
            fill=self.COLORS['white'],
            outline=self.COLORS['primary'],
            width=3
        )
        
        # 装饰条
        draw.rounded_rectangle(
            [50, 50, width-50, 60],
            radius=4,
            fill=self.COLORS['accent']
        )
        
        # 内容
        y = 80
        for line in lines:
            content = re.sub(r'^[┌├│└]', '  ', line)
            content = re.sub(r'[┐┤┘]$', '  ', content)
            if content.strip():
                draw.text((70, y), content.strip(), font=self.font, fill=self.COLORS['text'])
            y += 32
        
        return img


def process_document(converter, md_file, word_file):
    """处理单个文档"""
    doc_name = word_file.stem
    print(f"\n处理: {doc_name}")
    
    # 读取markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取ASCII艺术
    ascii_arts = []
    pattern = r'```\n?(.*?)```'
    for match in re.finditer(pattern, content, re.DOTALL):
        art = match.group(1).strip()
        if converter.is_valid_ascii_art(art):
            ascii_arts.append(art)
    
    if not ascii_arts:
        print(f"  ℹ 未找到有效ASCII艺术")
        return 0
    
    print(f"  发现 {len(ascii_arts)} 个有效ASCII艺术")
    
    # 生成图片
    generated = 0
    for art in ascii_arts:
        result = converter.generate_image(art, doc_name)
        if result:
            generated += 1
    
    print(f"  ✓ 生成 {generated} 个图片")
    return generated


def main():
    """主函数"""
    theory_dir = Path('research/theory')
    word_dir = Path('output/theory-docs')
    
    # 清理旧图片
    old_images = Path('output/theory-images')
    if old_images.exists():
        shutil.rmtree(old_images)
        print(f"✓ 清理旧图片: {old_images}")
    
    # 创建新目录
    new_images = Path('output/theory-images')
    new_images.mkdir(parents=True, exist_ok=True)
    
    # 创建转换器
    converter = OptimizedAsciiConverter(new_images)
    
    # 获取所有Word文件
    word_files = sorted(word_dir.glob('*.docx'))
    md_files = sorted(theory_dir.glob('*.md'))
    
    print(f"\n开始处理 {len(word_files)} 个文档...")
    print("="*70)
    
    total_images = 0
    total_arts = 0
    
    for i, word_file in enumerate(word_files):
        if i < len(md_files):
            count = process_document(converter, md_files[i], word_file)
            total_images += count
    
    print("\n" + "="*70)
    print(f"✓ 处理完成!")
    print(f"✓ 总图片数: {total_images}")
    print(f"✓ 图片位置: {new_images}")
    
    # 检查生成的图片
    generated_files = list(new_images.glob('*.png'))
    print(f"✓ 实际文件数: {len(generated_files)}")
    
    # 统计图片大小
    sizes = [os.path.getsize(f) for f in generated_files]
    avg_size = sum(sizes) / len(sizes) if sizes else 0
    print(f"✓ 平均文件大小: {avg_size:.0f} bytes")
    
    # 检查是否有空白图片（小于3KB）
    small_images = [f for f, s in zip(generated_files, sizes) if s < 3000]
    if small_images:
        print(f"⚠ 发现 {len(small_images)} 个小文件（可能空白）")
    else:
        print(f"✓ 所有图片质量良好")


if __name__ == '__main__':
    main()
