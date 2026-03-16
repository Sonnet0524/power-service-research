#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
武侯供电中心驻点工作研究报告Word生成器（8000字扩展版）
大幅扩充内容，达到5000-8000字要求
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os
from PIL import Image, ImageDraw, ImageFont


class BusinessDiagramGenerator:
    """专业商务图表生成器"""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 专业商务配色
        self.colors = {
            'primary': '#1B365D',      # 深海蓝
            'secondary': '#8B4513',    # 深棕色
            'tertiary': '#2E5A4C',     # 森林绿
            'accent': '#C9A227',       # 金色
            'white': '#FFFFFF',
            'text': '#333333',
            'border': '#CCCCCC'
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
    
    def create_workflow_diagram(self):
        """工作流程图"""
        width, height = 1400, 1800
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_font = self.get_font(38)
        draw.text((width//2, 60), "驻点工作流程", fill=self.colors['primary'], 
                 font=title_font, anchor="mm")
        
        sub_font = self.get_font(16)
        draw.text((width//2, 105), "Stationed Service Workflow", 
                 fill='#666666', font=sub_font, anchor="mm")
        
        phases = [
            {
                'title': '驻点前阶段',
                'subtitle': 'Pre-Stationed Phase',
                'time': 'T-1天',
                'color': self.colors['primary'],
                'items': ['查询小区信息', '获取重点客户清单', '查询历史记录', 
                         '制定工作计划', '准备物资资料'],
                'y': 220
            },
            {
                'title': '驻点中阶段',
                'subtitle': 'Execution Phase',
                'time': 'T日',
                'color': self.colors['secondary'],
                'items': ['公示牌张贴/检查', '加入/检查微信群', '重点客户走访',
                         '配电房检查', '应急资源采集', '其他工作'],
                'y': 720
            },
            {
                'title': '驻点后阶段',
                'subtitle': 'Post-Stationed Phase',
                'time': 'T+1~T+7天',
                'color': self.colors['tertiary'],
                'items': ['整理工作记录', '跟踪问题整改', '回访重点客户',
                         '处理客户诉求', '更新知识库', '总结归档'],
                'y': 1220
            }
        ]
        
        box_width = 1100
        box_height = 400
        left_margin = 150
        
        for i, phase in enumerate(phases):
            # 时间标签
            cy = phase['y'] + box_height//2
            r = 50
            draw.ellipse([50-r, cy-r, 50+r, cy+r], fill='#F5F5F5', 
                        outline=self.colors['primary'], width=3)
            time_font = self.get_font(20)
            draw.text((50, cy), phase['time'], fill=self.colors['primary'], 
                     font=time_font, anchor="mm")
            
            # 主框
            draw.rounded_rectangle([left_margin, phase['y'], 
                                   left_margin+box_width, phase['y']+box_height],
                                  radius=15, fill=phase['color'])
            
            # 标题
            title_font = self.get_font(28)
            draw.text((left_margin+box_width//2, phase['y']+50), phase['title'],
                     fill='white', font=title_font, anchor="mm")
            
            # 英文副标题
            eng_font = self.get_font(14)
            draw.text((left_margin+box_width//2, phase['y']+90), phase['subtitle'],
                     fill='#CCCCCC', font=eng_font, anchor="mm")
            
            # 工作内容
            item_font = self.get_font(19)
            for j, item in enumerate(phase['items'][:3]):
                y_pos = phase['y'] + 150 + j * 55
                draw.text((left_margin+60, y_pos), "•", fill=self.colors['accent'], font=item_font)
                draw.text((left_margin+90, y_pos), item, fill='white', font=item_font)
            
            for j, item in enumerate(phase['items'][3:]):
                y_pos = phase['y'] + 150 + j * 55
                draw.text((left_margin+box_width//2+50, y_pos), "•", 
                         fill=self.colors['accent'], font=item_font)
                draw.text((left_margin+box_width//2+80, y_pos), item, 
                         fill='white', font=item_font)
            
            # 连接箭头
            if i < len(phases) - 1:
                arrow_y1 = phase['y'] + box_height + 20
                arrow_y2 = phases[i+1]['y'] - 20
                draw.line([(width//2, arrow_y1), (width//2, arrow_y2)], 
                         fill=self.colors['primary'], width=5)
                draw.polygon([(width//2, arrow_y2), (width//2-10, arrow_y2-15),
                             (width//2+10, arrow_y2-15)], fill=self.colors['primary'])
        
        filepath = os.path.join(self.output_dir, 'workflow.png')
        img.save(filepath, 'PNG', dpi=(300, 300))
        return filepath
    
    def create_three_domain_diagram(self):
        """三大领域协同模型图"""
        width, height = 1600, 1000
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_font = self.get_font(38)
        draw.text((width//2, 70), "三大领域协同模型", fill=self.colors['primary'],
                 font=title_font, anchor="mm")
        
        sub_font = self.get_font(16)
        draw.text((width//2, 115), "Three-Domain Synergy Model", 
                 fill='#666666', font=sub_font, anchor="mm")
        
        domains = [
            {
                'title': '网格服务',
                'subtitle': 'Service First',
                'color': self.colors['primary'],
                'x': 250,
                'items': ['让客户找到人', '压降95598工单'],
                'arrow': '客户信息'
            },
            {
                'title': '用电检查',
                'subtitle': 'Information First',
                'color': self.colors['secondary'],
                'x': 800,
                'items': ['掌握设备状况', '消除安全隐患'],
                'arrow': '设备信息'
            },
            {
                'title': '应急保供',
                'subtitle': 'Resource First',
                'color': self.colors['tertiary'],
                'x': 1350,
                'items': ['建立知识库', '快速应急响应'],
                'arrow': ''
            }
        ]
        
        box_w = 360
        box_h = 450
        y_center = 520
        
        for i, domain in enumerate(domains):
            x = domain['x']
            
            # 阴影
            draw.rounded_rectangle([x-box_w//2+4, y_center-box_h//2+4, 
                                   x+box_w//2+4, y_center+box_h//2+4],
                                  radius=15, fill='#E0E0E0')
            
            # 主框
            draw.rounded_rectangle([x-box_w//2, y_center-box_h//2, 
                                   x+box_w//2, y_center+box_h//2],
                                  radius=15, fill=domain['color'])
            
            # 顶部金色条
            draw.rectangle([x-box_w//2, y_center-box_h//2, x+box_w//2, y_center-box_h//2+8],
                          fill=self.colors['accent'])
            
            # 中文标题
            title_font = self.get_font(26)
            draw.text((x, y_center-145), domain['title'], fill='white',
                     font=title_font, anchor="mm")
            
            # 英文副标题
            eng_font = self.get_font(13)
            draw.text((x, y_center-105), domain['subtitle'], 
                     fill='#CCCCCC', font=eng_font, anchor="mm")
            
            # 核心价值
            value_font = self.get_font(20)
            values = ['服务前置', '信息前置', '资源前置']
            draw.text((x, y_center-45), values[i], fill=self.colors['accent'],
                     font=value_font, anchor="mm")
            
            # 分隔线
            draw.line([x-120, y_center-5, x+120, y_center-5], 
                     fill='#CCCCCC', width=2)
            
            # 内容项
            item_font = self.get_font(18)
            for j, item in enumerate(domain['items']):
                y = y_center + 45 + j * 45
                draw.text((x-130, y), "✓", fill=self.colors['accent'], font=item_font)
                draw.text((x-100, y), item, fill='white', font=item_font)
            
            # 向右箭头
            if i < len(domains) - 1:
                next_x = domains[i+1]['x']
                arrow_x1 = x + box_w//2 + 15
                arrow_x2 = next_x - box_w//2 - 15
                
                draw.line([(arrow_x1, y_center), (arrow_x2, y_center)],
                         fill=domain['color'], width=4)
                draw.polygon([(arrow_x2, y_center), (arrow_x2-12, y_center-6),
                             (arrow_x2-12, y_center+6)], fill=domain['color'])
                
                # 标签
                if domain['arrow']:
                    label_font = self.get_font(14)
                    mid_x = (arrow_x1 + arrow_x2) // 2
                    draw.rectangle([mid_x-40, y_center-28, mid_x+40, y_center-5],
                                  fill='white', outline=domain['color'], width=1)
                    draw.text((mid_x, y_center-16), domain['arrow'],
                             fill=domain['color'], font=label_font, anchor="mm")
        
        # 底部返回弧线
        start_x = domains[2]['x'] - box_w//2
        end_x = domains[0]['x'] + box_w//2
        y_base = y_center + box_h//2 + 50
        
        points = []
        for t in range(0, 101, 3):
            t = t / 100
            x = start_x + (end_x - start_x) * t
            y = y_base + 80 * 4 * t * (1-t)
            points.append((x, y))
        
        for j in range(len(points)-1):
            draw.line([points[j], points[j+1]], fill=self.colors['tertiary'], width=3)
        
        draw.polygon([(end_x, y_base+15), (end_x-15, y_base+3), (end_x-15, y_base+27)],
                    fill=self.colors['tertiary'])
        
        label_font = self.get_font(15)
        draw.text((width//2, y_base+55), "提升信心 → 形成闭环",
                 fill=self.colors['tertiary'], font=label_font, anchor="mm")
        
        # 底部价值条
        draw.rectangle([200, 880, 1400, 950], fill='#FFF9E6', 
                      outline=self.colors['accent'], width=2)
        bottom_font = self.get_font(19)
        draw.text((width//2, 915), "核心价值：服务前置 + 信息前置 + 资源前置 = 客户满意度提升",
                 fill=self.colors['text'], font=bottom_font, anchor="mm")
        
        filepath = os.path.join(self.output_dir, 'three_domain.png')
        img.save(filepath, 'PNG', dpi=(300, 300))
        return filepath
    
    def create_information_flow_diagram(self):
        """信息前置机制流程图"""
        width, height = 1600, 900
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_font = self.get_font(38)
        draw.text((width//2, 70), "信息前置机制流程", fill=self.colors['primary'],
                 font=title_font, anchor="mm")
        
        sub_font = self.get_font(16)
        draw.text((width//2, 115), "Information Pre-positioning Framework",
                 fill='#666666', font=sub_font, anchor="mm")
        
        # 流程步骤
        steps = [
            {'name': '数据源', 'color': '#5A6C7D', 'x': 200,
             'desc': ['营销系统', 'PMS系统', '95598系统']},
            {'name': '数据汇聚', 'color': self.colors['primary'], 'x': 550,
             'desc': ['小区台账', '客户台账', '工作台账']},
            {'name': '信息推送', 'color': self.colors['secondary'], 'x': 900,
             'desc': ['重点客户清单', '自动推送']},
            {'name': '现场使用', 'color': self.colors['tertiary'], 'x': 1250,
             'desc': ['快速查询', '精准服务']},
        ]
        
        box_w = 260
        box_h = 220
        y_top = 280
        
        # 上方流程
        for i, step in enumerate(steps):
            x = step['x']
            
            # 阴影和主框
            draw.rounded_rectangle([x-box_w//2+3, y_top+3, x+box_w//2+3, y_top+box_h+3],
                                  radius=10, fill='#E8E8E8')
            draw.rounded_rectangle([x-box_w//2, y_top, x+box_w//2, y_top+box_h],
                                  radius=10, fill=step['color'])
            
            # 标题
            title_font = self.get_font(20)
            draw.text((x, y_top+35), step['name'], fill='white', font=title_font, anchor="mm")
            
            # 分隔线
            draw.line([x-box_w//2+20, y_top+65, x+box_w//2-20, y_top+65],
                     fill='#DDDDDD', width=1)
            
            # 描述
            desc_font = self.get_font(15)
            for j, desc in enumerate(step['desc']):
                y = y_top + 95 + j * 32
                draw.text((x, y), desc, fill='white', font=desc_font, anchor="mm")
            
            # 向右箭头
            if i < len(steps) - 1:
                next_x = steps[i+1]['x']
                arrow_x1 = x + box_w//2 + 10
                arrow_x2 = next_x - box_w//2 - 10
                
                draw.line([(arrow_x1, y_top+box_h//2), (arrow_x2, y_top+box_h//2)],
                         fill='#999999', width=3)
                draw.polygon([(arrow_x2, y_top+box_h//2), 
                             (arrow_x2-10, y_top+box_h//2-5),
                             (arrow_x2-10, y_top+box_h//2+5)], fill='#999999')
        
        # 下方数据更新框
        bottom_y = 620
        bottom_box = {'name': '数据更新', 'color': '#B8860B', 'x': 900}
        
        draw.rounded_rectangle([bottom_box['x']-box_w//2+3, bottom_y+3, 
                               bottom_box['x']+box_w//2+3, bottom_y+box_h+3],
                              radius=10, fill='#E8E8E8')
        draw.rounded_rectangle([bottom_box['x']-box_w//2, bottom_y, 
                               bottom_box['x']+box_w//2, bottom_y+box_h],
                              radius=10, fill=bottom_box['color'])
        
        title_font = self.get_font(20)
        draw.text((bottom_box['x'], bottom_y+35), bottom_box['name'],
                 fill='white', font=title_font, anchor="mm")
        
        draw.line([bottom_box['x']-box_w//2+20, bottom_y+65, 
                  bottom_box['x']+box_w//2-20, bottom_y+65],
                 fill='#DDDDDD', width=1)
        
        desc_font = self.get_font(15)
        draw.text((bottom_box['x'], bottom_y+105), "一次录入",
                 fill='white', font=desc_font, anchor="mm")
        draw.text((bottom_box['x'], bottom_y+140), "自动联动更新",
                 fill='white', font=desc_font, anchor="mm")
        
        # L型箭头
        start_point = (1250 + box_w//2 - 30, y_top + box_h)
        mid_point = (1250 + box_w//2 - 30, bottom_y)
        end_point = (bottom_box['x'] + box_w//2, bottom_y)
        
        draw.line([(start_point[0], start_point[1]), (mid_point[0], mid_point[1])],
                 fill=self.colors['tertiary'], width=3)
        draw.line([(mid_point[0], mid_point[1]), (end_point[0], end_point[1])],
                 fill=self.colors['tertiary'], width=3)
        draw.polygon([(end_point[0], end_point[1]), 
                     (end_point[0]-12, end_point[1]-6),
                     (end_point[0]-12, end_point[1]+6)], fill=self.colors['tertiary'])
        
        # 返回弧线
        start_x = bottom_box['x'] - box_w//2
        start_y = bottom_y + box_h//2
        end_x = 200 - box_w//2
        end_y = y_top + box_h//2
        
        points = []
        for t in range(0, 101, 3):
            t = t / 100
            x = start_x + (end_x - start_x) * t
            y = start_y - 120 * 4 * t * (1-t)
            points.append((x, y))
        
        for j in range(len(points)-1):
            draw.line([points[j], points[j+1]], fill=bottom_box['color'], width=3)
        
        draw.polygon([(end_x, end_y), (end_x+12, end_y-6), (end_x+12, end_y+6)],
                    fill=bottom_box['color'])
        
        # 标签
        label_font = self.get_font(14)
        draw.text((400, 750), "数据回流", fill=bottom_box['color'], font=label_font)
        
        draw.rounded_rectangle([1380, 520, 1560, 580], radius=5,
                              fill='#E8F5E9', outline=self.colors['tertiary'], width=2)
        draw.text((1470, 550), "闭环管理", fill=self.colors['tertiary'], 
                 font=self.get_font(16), anchor="mm")
        
        # 底部说明
        note_font = self.get_font(13)
        draw.text((width//2, 840), "机制说明：信息自动推送 → 现场精准服务 → 数据回流更新 → 形成管理闭环",
                 fill='#666666', font=note_font, anchor="mm")
        
        filepath = os.path.join(self.output_dir, 'information_flow.png')
        img.save(filepath, 'PNG', dpi=(300, 300))
        return filepath


# 继续Word文档生成部分...
