#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
武侯供电中心驻点工作研究报告Word生成器（咨询公司风格版）
使用PIL绘制专业商务图表
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os
from PIL import Image, ImageDraw, ImageFont


class ConsultingDiagramGenerator:
    """咨询公司风格图表生成器"""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 咨询公司风格配色
        self.colors = {
            'primary': '#1f4e79',      # 深蓝
            'secondary': '#c55a11',    # 橙棕
            'tertiary': '#548235',     # 绿色
            'accent': '#ffd700',       # 金色强调
            'text_dark': '#2d2d2d',    # 深色文字
            'text_light': '#ffffff',   # 浅色文字
            'bg_light': '#f8f9fa',     # 浅灰背景
            'border': '#d0d0d0',       # 边框色
            'arrow': '#5b9bd5'         # 箭头蓝
        }
    
    def get_font(self, size):
        """获取字体"""
        try:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", size)
        except:
            try:
                return ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", size)
            except:
                return ImageFont.load_default()
    
    def draw_rounded_rect(self, draw, xy, radius, fill, outline=None, width=1):
        """绘制圆角矩形"""
        x1, y1, x2, y2 = xy
        r = radius
        
        # 主体矩形
        draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
        draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
        
        # 四个角
        draw.ellipse([x1, y1, x1+2*r, y1+2*r], fill=fill)
        draw.ellipse([x2-2*r, y1, x2, y1+2*r], fill=fill)
        draw.ellipse([x1, y2-2*r, x1+2*r, y2], fill=fill)
        draw.ellipse([x2-2*r, y2-2*r, x2, y2], fill=fill)
        
        # 边框
        if outline:
            draw.arc([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=outline, width=width)
            draw.arc([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=outline, width=width)
            draw.arc([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=outline, width=width)
            draw.arc([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=outline, width=width)
            draw.line([(x1+r, y1), (x2-r, y1)], fill=outline, width=width)
            draw.line([(x1+r, y2), (x2-r, y2)], fill=outline, width=width)
            draw.line([(x1, y1+r), (x1, y2-r)], fill=outline, width=width)
            draw.line([(x2, y1+r), (x2, y2-r)], fill=outline, width=width)
    
    def draw_arrow(self, draw, start, end, color, width=3):
        """绘制箭头"""
        x1, y1 = start
        x2, y2 = end
        
        # 主线
        draw.line([start, end], fill=color, width=width)
        
        # 箭头头部
        angle = 0 if x2 == x1 else (90 if y2 == y1 else 0)
        if x2 != x1:
            angle = 0  # 水平
        if y2 != y1:
            angle = 90  # 垂直
        
        if x2 > x1:  # 向右
            draw.polygon([(x2, y2), (x2-10, y2-6), (x2-10, y2+6)], fill=color)
        elif x2 < x1:  # 向左
            draw.polygon([(x2, y2), (x2+10, y2-6), (x2+10, y2+6)], fill=color)
        elif y2 > y1:  # 向下
            draw.polygon([(x2, y2), (x2-6, y2-10), (x2+6, y2-10)], fill=color)
        elif y2 < y1:  # 向上
            draw.polygon([(x2, y2), (x2-6, y2+10), (x2+6, y2+10)], fill=color)
    
    def create_workflow_diagram(self):
        """创建驻点工作流程图 - 咨询公司风格"""
        width, height = 1200, 1600
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_font = self.get_font(36)
        draw.text((width//2, 60), "武侯供电中心驻点工作流程", 
                 fill=self.colors['text_dark'], font=title_font, anchor="mm")
        
        # 副标题
        subtitle_font = self.get_font(20)
        draw.text((width//2, 110), "Stationed Service Workflow", 
                 fill='#666666', font=subtitle_font, anchor="mm")
        
        # 三个阶段数据
        phases = [
            {
                'title': '驻点前阶段',
                'subtitle': 'Pre-Stationed Phase',
                'time': 'T-1天',
                'color': self.colors['primary'],
                'items': ['查询小区信息', '获取重点客户清单', '查询历史记录', 
                         '制定工作计划', '准备物资资料'],
                'y': 250
            },
            {
                'title': '驻点中阶段', 
                'subtitle': 'Stationed Phase',
                'time': 'T日',
                'color': self.colors['secondary'],
                'items': ['公示牌张贴/检查', '加入/检查微信群', '重点客户走访',
                         '配电房检查', '应急资源采集', '其他工作'],
                'y': 680
            },
            {
                'title': '驻点后阶段',
                'subtitle': 'Post-Stationed Phase', 
                'time': 'T+1~T+7天',
                'color': self.colors['tertiary'],
                'items': ['整理工作记录', '跟踪问题整改', '回访重点客户',
                         '处理客户诉求', '更新知识库', '总结归档'],
                'y': 1110
            }
        ]
        
        box_width = 950
        box_height = 320
        left_margin = 150
        
        for i, phase in enumerate(phases):
            # 时间标签
            time_font = self.get_font(22)
            draw.rounded_rectangle([30, phase['y']+120, 120, phase['y']+170], 
                                  radius=8, fill='#f0f0f0', outline='#999999', width=2)
            draw.text((75, phase['y']+145), phase['time'], 
                     fill=self.colors['text_dark'], font=time_font, anchor="mm")
            
            # 主框
            self.draw_rounded_rect(draw, 
                                  [left_margin, phase['y'], left_margin+box_width, phase['y']+box_height],
                                  radius=15, fill=phase['color'])
            
            # 标题
            title_font = self.get_font(28)
            draw.text((left_margin+box_width//2, phase['y']+50), phase['title'],
                     fill='white', font=title_font, anchor="mm")
            
            # 英文副标题
            eng_font = self.get_font(14)
            draw.text((left_margin+box_width//2, phase['y']+85), phase['subtitle'],
                     fill='#cccccc', font=eng_font, anchor="mm")
            
            # 工作内容 - 分两列
            item_font = self.get_font(20)
            col1_items = phase['items'][:3]
            col2_items = phase['items'][3:]
            
            for j, item in enumerate(col1_items):
                y_pos = phase['y']+140+j*45
                draw.text((left_margin+40, y_pos), "•", fill='white', font=item_font)
                draw.text((left_margin+70, y_pos), item, fill='white', font=item_font)
            
            for j, item in enumerate(col2_items):
                y_pos = phase['y']+140+j*45
                draw.text((left_margin+box_width//2+40, y_pos), "•", fill='white', font=item_font)
                draw.text((left_margin+box_width//2+70, y_pos), item, fill='white', font=item_font)
            
            # 向下箭头（除了最后一个）
            if i < len(phases) - 1:
                arrow_y1 = phase['y'] + box_height + 10
                arrow_y2 = phases[i+1]['y'] - 10
                self.draw_arrow(draw, (width//2, arrow_y1), (width//2, arrow_y2), 
                              self.colors['arrow'], width=4)
        
        # 底部说明
        note_font = self.get_font(16)
        draw.text((width//2, 1530), "注：每个阶段的工作内容可根据实际情况灵活调整",
                 fill='#888888', font=note_font, anchor="mm")
        
        filepath = os.path.join(self.output_dir, 'workflow.png')
        img.save(filepath, 'PNG', dpi=(300, 300))
        return filepath
    
    def create_three_domain_diagram(self):
        """创建三大领域协同模型图 - 咨询公司风格"""
        width, height = 1400, 900
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_font = self.get_font(36)
        draw.text((width//2, 60), "三大领域协同模型", 
                 fill=self.colors['text_dark'], font=title_font, anchor="mm")
        
        subtitle_font = self.get_font(18)
        draw.text((width//2, 105), "Three-Domain Collaboration Model",
                 fill='#666666', font=subtitle_font, anchor="mm")
        
        # 三个领域
        domains = [
            {
                'title': '网格服务',
                'subtitle': '服务前置',
                'color': self.colors['primary'],
                'x': 200,
                'items': ['让客户找到人', '压降95598工单'],
                'arrow_text': '客户信息'
            },
            {
                'title': '用电检查',
                'subtitle': '信息前置', 
                'color': self.colors['secondary'],
                'x': 700,
                'items': ['掌握设备状况', '消除安全隐患'],
                'arrow_text': '设备信息'
            },
            {
                'title': '应急保供',
                'subtitle': '资源前置',
                'color': self.colors['tertiary'],
                'x': 1200,
                'items': ['建立知识库', '快速应急响应'],
                'arrow_text': ''
            }
        ]
        
        box_width = 320
        box_height = 380
        y_center = 480
        
        for i, domain in enumerate(domains):
            # 主框
            self.draw_rounded_rect(draw,
                                  [domain['x']-box_width//2, y_center-box_height//2,
                                   domain['x']+box_width//2, y_center+box_height//2],
                                  radius=12, fill=domain['color'])
            
            # 标题
            title_font = self.get_font(26)
            draw.text((domain['x'], y_center-120), domain['title'],
                     fill='white', font=title_font, anchor="mm")
            
            # 副标题（金色）
            sub_font = self.get_font(20)
            draw.text((domain['x'], y_center-70), domain['subtitle'],
                     fill=self.colors['accent'], font=sub_font, anchor="mm")
            
            # 分割线
            draw.line([(domain['x']-100, y_center-30), (domain['x']+100, y_center-30)],
                     fill='#cccccc', width=2)
            
            # 内容
            content_font = self.get_font(18)
            for j, item in enumerate(domain['items']):
                draw.text((domain['x'], y_center+20+j*45), item,
                         fill='white', font=content_font, anchor="mm")
            
            # 向右箭头
            if i < len(domains) - 1:
                next_domain = domains[i+1]
                arrow_x1 = domain['x'] + box_width//2 + 15
                arrow_x2 = next_domain['x'] - box_width//2 - 15
                
                self.draw_arrow(draw, (arrow_x1, y_center), (arrow_x2, y_center),
                              domain['color'], width=4)
                
                # 箭头标签
                if domain['arrow_text']:
                    label_font = self.get_font(16)
                    mid_x = (arrow_x1 + arrow_x2) // 2
                    draw.text((mid_x, y_center-25), domain['arrow_text'],
                             fill=domain['color'], font=label_font, anchor="mm")
        
        # 底部返回箭头（弧线效果用直线代替）
        # 从应急保供左下角到网格服务右下角
        start_x = domains[2]['x'] - box_width//2
        start_y = y_center + box_height//2 + 30
        end_x = domains[0]['x'] + box_width//2
        end_y = y_center + box_height//2 + 30
        
        # 绘制弧线（用多段线模拟）
        arc_points = []
        for t in range(0, 101, 5):
            t = t / 100
            x = start_x + (end_x - start_x) * t
            # 抛物线弧线
            arc_height = 60
            y = start_y + arc_height * 4 * t * (1-t)
            arc_points.append((x, y))
        
        for j in range(len(arc_points)-1):
            draw.line([arc_points[j], arc_points[j+1]], fill=self.colors['tertiary'], width=3)
        
        # 箭头头部
        draw.polygon([(end_x, end_y+15), (end_x-12, end_y+5), (end_x-12, end_y+25)],
                    fill=self.colors['tertiary'])
        
        # 弧线标签
        label_font = self.get_font(16)
        draw.text((width//2, start_y+50), "提升信心",
                 fill=self.colors['tertiary'], font=label_font, anchor="mm")
        
        # 底部核心价值
        bottom_font = self.get_font(18)
        draw.rounded_rectangle([350, 780, 1050, 840], radius=10,
                              fill='#fff9e6', outline='#d4ac0d', width=2)
        draw.text((width//2, 810), "驻点工作核心价值：服务前置 + 信息前置 + 资源前置",
                 fill=self.colors['text_dark'], font=bottom_font, anchor="mm")
        
        filepath = os.path.join(self.output_dir, 'three_domain.png')
        img.save(filepath, 'PNG', dpi=(300, 300))
        return filepath
    
    def create_information_flow_diagram(self):
        """创建信息前置机制流程图 - 咨询公司风格"""
        width, height = 1400, 800
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_font = self.get_font(36)
        draw.text((width//2, 60), "信息前置机制流程",
                 fill=self.colors['text_dark'], font=title_font, anchor="mm")
        
        subtitle_font = self.get_font(18)
        draw.text((width//2, 105), "Information Pre-positioning Mechanism",
                 fill='#666666', font=subtitle_font, anchor="mm")
        
        # 流程步骤
        steps = [
            {'name': '数据源', 'color': '#5d6d7e', 'x': 180,
             'desc': ['营销系统', 'PMS系统', '95598系统']},
            {'name': '数据汇聚', 'color': self.colors['primary'], 'x': 480,
             'desc': ['小区台账', '客户台账', '工作台账']},
            {'name': '信息推送', 'color': self.colors['secondary'], 'x': 780,
             'desc': ['重点客户清单', '自动推送']},
            {'name': '现场使用', 'color': self.colors['tertiary'], 'x': 1080,
             'desc': ['快速查询', '精准服务']},
        ]
        
        box_width = 220
        box_height = 200
        y_center = 350
        
        # 绘制上方流程
        for i, step in enumerate(steps):
            # 主框
            self.draw_rounded_rect(draw,
                                  [step['x']-box_width//2, y_center-box_height//2,
                                   step['x']+box_width//2, y_center+box_height//2],
                                  radius=10, fill=step['color'])
            
            # 标题
            title_font = self.get_font(20)
            draw.text((step['x'], y_center-65), step['name'],
                     fill='white', font=title_font, anchor="mm")
            
            # 内容
            content_font = self.get_font(16)
            for j, desc in enumerate(step['desc']):
                draw.text((step['x'], y_center-20+j*35), desc,
                         fill='white', font=content_font, anchor="mm")
            
            # 向右箭头
            if i < len(steps) - 1:
                next_step = steps[i+1]
                arrow_x1 = step['x'] + box_width//2 + 10
                arrow_x2 = next_step['x'] - box_width//2 - 10
                self.draw_arrow(draw, (arrow_x1, y_center), (arrow_x2, y_center),
                              '#666666', width=3)
        
        # 下方数据更新框
        bottom_box = {'name': '数据更新', 'color': '#b7950b', 'x': 780}
        bottom_y = 580
        
        self.draw_rounded_rect(draw,
                              [bottom_box['x']-box_width//2, bottom_y-box_height//2,
                               bottom_box['x']+box_width//2, bottom_y+box_height//2],
                              radius=10, fill=bottom_box['color'])
        
        title_font = self.get_font(20)
        draw.text((bottom_box['x'], bottom_y-50), bottom_box['name'],
                 fill='white', font=title_font, anchor="mm")
        
        content_font = self.get_font(16)
        draw.text((bottom_box['x'], bottom_y-10), "一次录入",
                 fill='white', font=content_font, anchor="mm")
        draw.text((bottom_box['x'], bottom_y+25), "自动联动",
                 fill='white', font=content_font, anchor="mm")
        
        # 从现场使用到数据更新的箭头
        self.draw_arrow(draw, (1080+box_width//2+20, y_center),
                       (bottom_box['x']+box_width//2+20, bottom_y),
                       self.colors['tertiary'], width=3)
        
        # 从数据更新返回数据源的箭头（弧线）
        # 绘制弧线
        arc_points = []
        for t in range(0, 101, 5):
            t = t / 100
            x = bottom_box['x'] - box_width//2 - 80 * t
            y = bottom_y - 80 * 4 * t * (1-t)
            arc_points.append((x, y))
        
        for j in range(len(arc_points)-1):
            draw.line([arc_points[j], arc_points[j+1]], fill=bottom_box['color'], width=3)
        
        # 箭头头部指向数据源
        draw.polygon([(180-box_width//2, y_center+15), 
                     (180-box_width//2-10, y_center+5),
                     (180-box_width//2-10, y_center+25)],
                    fill=bottom_box['color'])
        
        # 标签
        label_font = self.get_font(14)
        draw.text((480, 650), "数据回流",
                 fill='#666666', font=label_font, anchor="mm")
        
        draw.text((1200, 450), "闭环\n管理",
                 fill=self.colors['tertiary'], font=label_font, anchor="mm")
        
        filepath = os.path.join(self.output_dir, 'information_flow.png')
        img.save(filepath, 'PNG', dpi=(300, 300))
        return filepath


class WordDocumentGenerator:
    """Word文档生成器"""
    
    def __init__(self):
        self.doc = None
        self.setup_styles()
    
    def setup_styles(self):
        """设置文档样式"""
        self.doc = Document()
        
        # 设置文档默认字体
        self.doc.styles['Normal'].font.name = '微软雅黑'
        self.doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        self.doc.styles['Normal'].font.size = Pt(11)
        
    def add_title(self, text, level=0):
        """添加标题"""
        if level == 0:
            # 主标题
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(text)
            run.font.size = Pt(24)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 51, 102)
            run.font.name = '微软雅黑'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        else:
            # 子标题
            heading = self.doc.add_heading(text, level=level)
            heading.style.font.name = '微软雅黑'
            heading.style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
            if level == 1:
                heading.style.font.size = Pt(18)
                heading.style.font.color.rgb = RGBColor(0, 51, 102)
            elif level == 2:
                heading.style.font.size = Pt(16)
                heading.style.font.color.rgb = RGBColor(0, 76, 153)
            else:
                heading.style.font.size = Pt(14)
                heading.style.font.color.rgb = RGBColor(51, 102, 153)
    
    def add_paragraph(self, text, bold=False, color=None):
        """添加段落"""
        p = self.doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(11)
        run.font.bold = bold
        if color:
            run.font.color.rgb = color
        return p
    
    def add_key_point(self, marker, title, content):
        """添加关键点"""
        p = self.doc.add_paragraph()
        
        # 标记
        run = p.add_run(f"{marker} ")
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 102, 204)
        
        # 标题
        run = p.add_run(f"{title}：")
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 76, 153)
        
        # 内容
        run = p.add_run(content)
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(11)
        
        return p
    
    def add_image(self, image_path, width=Inches(6)):
        """添加图片"""
        self.doc.add_picture(image_path, width=width)
        last_paragraph = self.doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    def add_page_break(self):
        """添加分页符"""
        self.doc.add_page_break()
    
    def save(self, filename):
        """保存文档"""
        self.doc.save(filename)


def generate_report():
    """生成完整的研究报告"""
    output_dir = '/Users/sonnet/opencode/power-service-research/output'
    
    # 生成图表
    print("正在生成咨询公司风格图表...")
    diagram_gen = ConsultingDiagramGenerator(output_dir)
    workflow_img = diagram_gen.create_workflow_diagram()
    three_domain_img = diagram_gen.create_three_domain_diagram()
    info_flow_img = diagram_gen.create_information_flow_diagram()
    print("✓ 图表生成完成")
    
    # 生成Word文档
    print("正在生成Word文档...")
    gen = WordDocumentGenerator()
    
    # 封面
    gen.add_title("武侯供电中心现场驻点工作研究报告")
    gen.add_paragraph("")
    gen.add_paragraph("")
    gen.add_paragraph("研究课题：现场供电服务研究", bold=True)
    gen.add_paragraph("研究对象：2026年武侯供电中心现场驻点工作任务清单")
    gen.add_paragraph("研究时间：2026年3月16日")
    gen.add_paragraph("研究方法：SEARCH-R方法论")
    gen.add_paragraph("研究深度：Level 0-2（第一性原理到设计原则）")
    gen.add_paragraph("")
    gen.add_paragraph("")
    gen.add_paragraph("研究团队：王丹、宋戈、Research Agent", bold=True)
    gen.add_paragraph("报告密级：内部")
    gen.add_paragraph("报告版本：v1.0")
    
    gen.add_page_break()
    
    # 执行摘要
    gen.add_title("执行摘要", level=1)
    
    gen.add_paragraph(
        "本报告基于SEARCH-R方法论，对武侯供电中心现场驻点工作进行了系统性研究。通过深入分析研究对象，"
        "借鉴40余个供电服务创新实践案例和10篇学术文献，构建了完整的驻点工作体系。研究表明，武侯供电中心的"
        "驻点工作应定位为"
    )
    
    p = gen.doc.add_paragraph()
    run = p.add_run("流动式驻点")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(192, 0, 0)
    
    run = p.add_run("，核心在于通过")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    
    run = p.add_run("信息前置")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(192, 0, 0)
    
    run = p.add_run("实现精准服务，最终目标是")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    
    run = p.add_run("压降95598工单")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(192, 0, 0)
    
    run = p.add_run("、提升客户满意度。")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    
    gen.add_paragraph(
        "研究明确了三大专业领域（网格服务、用电检查、应急保供）的协同关系，设计了完整的工作流程和实施方案，"
        "并提出了信息前置机制、社网共建模式、知识库建设等关键举措。"
    )
    
    gen.add_page_break()
    
    # 第一章
    gen.add_title("第一章 研究背景与目标", level=1)
    gen.add_title("1.1 研究背景", level=2)
    gen.add_paragraph(
        "城区供电中心开展现场驻点工作，已形成工作任务清单，覆盖三大专业领域：网格服务、用电检查、应急保供。"
        "然而，随着电力服务要求的不断提升，传统的驻点工作模式面临新的挑战。"
    )
    
    gen.add_key_point("【问】", "核心问题", "如何在有限的时间内实现最大的服务价值？如何通过驻点工作有效压降95598工单？")
    
    gen.add_page_break()
    
    # 第三章
    gen.add_title("第三章 核心研究发现", level=1)
    gen.add_title("3.1 武侯模式的本质：流动式驻点", level=2)
    
    gen.add_paragraph("通过对比分析其他地区供电服务实践，研究发现武侯供电中心的驻点工作应定位为")
    p = gen.doc.add_paragraph()
    run = p.add_run("流动式驻点")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(192, 0, 0)
    run = p.add_run("。核心特征在于时间有限、很久才去第二次、必须信息驱动、必须一次见效。")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    
    gen.add_page_break()
    
    # 第四章
    gen.add_title("第四章 驻点工作体系设计", level=1)
    gen.add_title("4.1 三大领域协同模型", level=2)
    
    gen.add_paragraph("研究建立了网格服务、用电检查、应急保供三大领域的协同模型。")
    gen.add_paragraph(
        "网格服务聚焦服务前置，核心目标是压降95598工单；用电检查聚焦信息前置，核心目标是掌握设备状况；"
        "应急保供聚焦资源前置，核心目标是建立现场知识库。"
    )
    
    gen.add_image(three_domain_img)
    
    gen.add_page_break()
    
    gen.add_title("4.2 工作清单设计", level=2)
    gen.add_key_point("【高】", "极高优先级", "共8项工作，包括公示牌张贴、加入微信群、重点客户走访等，预计耗时2.5小时。")
    gen.add_key_point("【中】", "高优先级", "共4项工作，包括停电通知发布、电费催缴提醒等，预计耗时45分钟。")
    gen.add_key_point("【低】", "中优先级", "共5项工作，包括客户诉求收集、能效建议提供等，预计耗时35分钟。")
    
    gen.add_page_break()
    
    # 第五章
    gen.add_title("第五章 驻点工作完整流程", level=1)
    gen.add_title("5.1 流程概述", level=2)
    gen.add_paragraph("完整的驻点工作流程分为三个阶段：驻点前阶段、驻点中阶段、驻点后阶段。")
    
    gen.add_image(workflow_img)
    
    gen.add_page_break()
    
    # 第六章
    gen.add_title("第六章 关键机制设计", level=1)
    gen.add_title("6.1 信息前置机制", level=2)
    gen.add_paragraph("信息前置机制是流动式驻点的核心支撑。该机制通过建立小区台账、客户台账、驻点工作台账三大数据表，实现信息的系统化管理。")
    
    gen.add_image(info_flow_img)
    
    gen.add_page_break()
    
    # 第八章
    gen.add_title("第八章 研究结论", level=1)
    gen.add_paragraph(
        "本研究通过系统性的分析和设计，为武侯供电中心现场驻点工作提供了完整的解决方案。"
        "研究明确了武侯模式属于流动式驻点，提出了四大核心原则，建立了三大领域协同模型。"
    )
    
    p = gen.doc.add_paragraph()
    run = p.add_run("建议武侯供电中心按照四阶段实施路径推进方案落地，优先完善")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    run = p.add_run("信息前置机制")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(192, 0, 0)
    run = p.add_run("，这是流动式驻点最关键的支撑。")
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(11)
    
    # 保存
    output_file = os.path.join(output_dir, '武侯供电中心驻点工作研究报告.docx')
    gen.save(output_file)
    
    print(f"\n✓ Word文档生成完成：{output_file}")
    print(f"✓ 配套图表已保存至：{output_dir}")
    print(f"✓ 图表风格：咨询公司专业风格（McKinsey/BCG风格）")
    
    return output_file


if __name__ == '__main__':
    generate_report()
