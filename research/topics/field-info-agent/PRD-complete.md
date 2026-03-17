# 现场信息收集Agent - 完整PRD文档

---

**文档版本**: v1.0  
**创建日期**: 2026-03-17  
**最后更新**: 2026-03-17  
**研究方法论**: SEARCH-R  

---

## 一、SEARCH-R分析摘要

### 1.1 调研结论（Explore阶段）

#### 1.1.1 企业微信API能力调研

**核心发现**：

| 能力项 | 支持情况 | 详细说明 |
|--------|----------|----------|
| **智能机器人API** | ✅ 完整支持 | 2026年3月最新更新，支持接收消息、事件、被动回复、主动推送、长连接模式 |
| **消息类型** | ✅ 全面支持 | 文字、图片、语音、视频、文件、位置、链接、小程序卡片 |
| **文档API** | ✅ 支持 | 新建文档、编辑内容、获取表格数据、管理智能表格 |
| **微盘API** | ✅ 支持 | 文件上传、下载、分享、权限管理 |
| **回调机制** | ✅ 支持 | 接收用户消息、事件推送、加解密方案 |
| **会话存档** | ✅ 支持 | 可获取聊天记录（需开通） |

**关键限制**：
- 必须在线使用（无离线能力）
- 需要通过企业微信管理员审批应用权限
- 消息有频率限制（每应用每企业最多20次/秒）

#### 1.1.2 WPS开放平台API能力调研

**核心发现**：

| 能力项 | 支持情况 | 详细说明 |
|--------|----------|----------|
| **多维表格API** | ✅ 完整支持 | 查询记录、添加记录、更新记录、删除记录、批量操作 |
| **文档API** | ✅ 支持 | 创建文档、获取文档内容、编辑文档、管理权限 |
| **表格操作** | ✅ 支持 | 读取单元格、写入数据、格式化、公式计算 |
| **文件存储** | ✅ 支持 | 云文档管理、文件夹操作、分享链接生成 |
| **在线协作** | ✅ 支持 | 多人实时编辑、评论、历史版本 |
| **AirScript** | ✅ 支持 | 服务端JavaScript脚本自动化 |

**关键限制**：
- 需要申请API权限（管理员审批）
- 调用频率限制（根据套餐不同）
- 文件大小限制（上传文件最大100MB）

#### 1.1.3 OpenClaw集成分析

**适配性评估**：

| 维度 | 评估 | 说明 |
|------|------|------|
| **架构匹配度** | ⭐⭐⭐⭐⭐ | OpenClaw的Channel架构天然支持企业微信Provider |
| **Skill扩展性** | ⭐⭐⭐⭐⭐ | 可通过Skills扩展WPS操作能力 |
| **工具集成** | ⭐⭐⭐⭐ | 需开发WPS API Tool，但技术可行 |
| **部署方式** | ⭐⭐⭐⭐ | 云端部署符合用户要求 |

**集成模式**：
```
┌─────────────────────────────────────────────┐
│  企业微信平台（消息入口）                     │
│  - 接收用户消息                              │
│  - 推送Agent回复                             │
└────────────────┬────────────────────────────┘
                 │ 企业微信回调/API
                 ▼
┌─────────────────────────────────────────────┐
│  OpenClaw Gateway（云端部署）               │
│  - Channel: 企业微信Provider                │
│  - Session: 会话管理                        │
│  - Skills: 业务逻辑                         │
│    * StationWorkGuide（驻点工作引导）       │
│    * AutoDocGeneration（文档自动生成）      │
│    * EmergencyGuide（应急处置）             │
└────────────────┬────────────────────────────┘
                 │ HTTPS/REST API
                 ▼
┌─────────────────────────────────────────────┐
│  WPS开放平台（数据存储）                     │
│  - 多维表格：结构化数据                      │
│  - 云文档：文件存储                          │
│  - 在线编辑：协作查看                        │
└─────────────────────────────────────────────┘
```

---

## 二、产品需求规格说明

### 2.1 产品概述

**产品名称**: 现场信息收集Agent（FieldInfoCollector）  
**产品定位**: 面向供电所现场工作人员的AI助手，通过企业微信交互，实现驻点工作信息采集和文档自动生成  
**核心价值**: 让现场人员"开口说、随手拍"，Agent自动完成信息结构化、文档生成、知识沉淀

### 2.2 用户角色

| 角色 | 描述 | 主要场景 |
|------|------|----------|
| **客户经理** | 现场驻点工作人员 | 开展驻点工作、采集信息、走访客户 |
| **供电所长** | 供电所管理人员 | 查看工作汇总、审核重要问题、接收通知 |
| **抢修人员** | 应急处置人员 | 接收应急信息、查看应急指引 |
| **客服人员** | 后台客服人员 | 查看客户信息、处理问题工单 |

### 2.3 功能需求

#### 2.3.1 驻点工作引导（FR-001~FR-020）

**FR-001: 工作启动**
- 用户通过企业微信命令"/start-station-work 小区名"启动驻点工作
- Agent查询小区历史信息，生成任务清单
- 推送工作建议和历史遗留问题

**FR-002: 配电房信息采集**
- 引导用户拍摄配电房入口照片
- 语音记录配电房位置
- OCR识别变压器铭牌信息
- 记录设备运行状态
- 标记设备缺陷和隐患

**FR-003: 客户走访记录**
- 根据历史数据推荐走访客户
- 语音记录客户反馈
- 分类问题类型（停电、电费、服务、其他）
- 标记客户满意度
- 标记是否需要回访

**FR-004: 应急信息采集**
- 引导拍摄发电车进入点、停放点、接入点
- 记录电缆型号和长度
- 记录物业应急联系人
- 生成应急接入方案

**FR-005: 智能审核**
- 自动检查照片清晰度
- 验证必填字段完整性
- 标记缺失信息
- 提示补充采集

#### 2.3.2 文档自动生成（FR-021~FR-030）

**FR-021: 小区供电简报**
- 自动汇总小区基础信息
- 统计配电设施情况
- 汇总客户走访情况
- 生成Word/PDF文档
- 保存到WPS云文档

**FR-022: 应急发电指引**
- 提取应急接入点信息
- 汇总电缆型号和长度
- 整理物业联系人
- 生成带地图指引的文档
- 包含现场照片

**FR-023: 驻点工作总结**
- 汇总本次驻点所有采集信息
- 统计工作量和完成情况
- 列出发现问题和处理措施
- 生成工作总结文档

**FR-024: 优质服务简报**
- 汇总客户走访记录
- 统计满意度分布
- 列出典型问题和案例
- 生成服务简报（月度/季度）

#### 2.3.3 应急处置（FR-031~FR-040）

**FR-031: 应急事件启动**
- 用户通过"/emergency 类型 地点"启动应急
- Agent立即查询应急资料
- 推送应急联系人清单
- 启动应急处理流程

**FR-032: 敏感客户关怀**
- 自动查询停电影响范围内的敏感客户
- 推送敏感客户清单（老人、孕妇、重要用户）
- 提供一键拨打功能
- 记录关怀情况

**FR-033: 应急方案推送**
- 根据小区自动调取应急发电指引
- 推送到场路线和接入点信息
- 提供导航链接
- 实时更新处理进展

**FR-034: 过程记录**
- 记录应急处理时间节点
- 保存现场照片
- 记录处理措施
- 生成应急处理报告

#### 2.3.4 通知系统（FR-041~FR-050）

**FR-041: 工作完成通知**
- 触发条件：驻点工作结束
- 接收人：本人、所长
- 内容：工作完成情况、生成文档链接

**FR-042: 问题发现通知**
- 触发条件：发现设备缺陷或隐患
- 接收人：本人、所长、专责
- 内容：问题描述、位置、照片、建议措施
- 优先级：高

**FR-043: 日报汇总**
- 触发条件：每天18:00
- 接收人：所长、当日工作人员
- 内容：当日工作汇总统计

**FR-044: 周报汇总**
- 触发条件：每周五18:00
- 接收人：所长、全员
- 内容：本周工作统计、问题汇总、下周计划

**FR-045: 应急事件通知**
- 触发条件：启动应急处置
- 接收人：现场人员、所长、抢修队
- 内容：事件类型、地点、影响范围、应急资料
- 优先级：紧急

### 2.4 非功能需求

#### 2.4.1 数据权限（NFR-001~NFR-005）

**NFR-001: 供电所内共享**
- 本供电所人员可查看、编辑所有数据
- 其他供电所人员不可见
- 所长拥有审核、导出权限

**NFR-002: 按小区分文件夹**
```
武侯供电中心/
├── 阳光小区/
│   ├── 小区基础信息.docx
│   ├── 供电简报/
│   ├── 配电房/
│   ├── 客户走访/
│   └── 驻点工作/
├── 锦绣花园/
└── 金色家园/
```

**NFR-003: 在线使用**
- 不支持离线模式
- 网络中断时提示用户检查网络
- 不缓存本地数据

#### 2.4.2 性能需求（NFR-006~NFR-010）

**NFR-006: 响应时间**
- 消息回复延迟 < 2秒
- 文档生成时间 < 30秒
- 照片上传时间 < 10秒（正常网络）

**NFR-007: 并发支持**
- 支持50人同时使用
- 支持多供电所独立部署

**NFR-008: 可用性**
- 服务可用性 99.5%
- 故障恢复时间 < 30分钟

#### 2.4.3 安全需求（NFR-011~NFR-015）

**NFR-011: 数据加密**
- 传输加密：HTTPS/TLS 1.2+
- 存储加密：WPS云文档自带加密
- 敏感字段加密存储

**NFR-012: 访问控制**
- 企业微信身份认证
- 供电所级别的数据隔离
- 操作日志记录

**NFR-013: 审计日志**
- 记录所有数据操作
- 保留期限：365天
- 支持按用户、时间、操作类型查询

---

## 三、技术架构设计

### 3.1 系统架构

```yaml
# 架构分层
layers:
  presentation:
    name: 交互层
    components:
      - 企业微信APP（用户入口）
      - WPS云文档（文档查看编辑）
    
  gateway:
    name: 网关层
    components:
      - OpenClaw Gateway
      - 企业微信Provider（Channel）
      - 消息路由与分发
    
  business:
    name: 业务层
    components:
      - StationWorkGuide Skill
      - AutoDocGeneration Skill
      - EmergencyGuide Skill
      - NotificationService
    
  tools:
    name: 工具层
    components:
      - 企业微信API Tool
      - WPS API Tool
      - 百度语音识别 Tool
      - OCR识别 Tool
      - 本地NLP Tool
    
  data:
    name: 数据层
    components:
      - WPS多维表格（结构化数据）
      - WPS云文档（文件存储）
      - Redis（会话缓存）
```

### 3.2 OpenClaw配置

```yaml
# openclaw.config.yaml
name: FieldInfoCollector
version: 1.0.0

deployment:
  type: cloud
  platform: docker
  
channels:
  wecom:
    enabled: true
    provider: official
    corp_id: "${WECOM_CORP_ID}"
    agent_id: "${WECOM_AGENT_ID}"
    secret: "${WECOM_SECRET}"
    callback_url: "https://agent-domain.com/webhook/wecom"
    token: "${WECOM_TOKEN}"
    encoding_aes_key: "${WECOM_AES_KEY}"
    
skills:
  station_work_guide:
    enabled: true
    entry_commands:
      - "/start-station-work"
      - "/collect-power-room"
      - "/collect-customer-visit"
      - "/collect-emergency-access"
    
  auto_doc_generation:
    enabled: true
    entry_commands:
      - "/generate-doc"
    doc_types:
      - power_briefing
      - emergency_guide
      - service_report
      - work_summary
    
  emergency_guide:
    enabled: true
    entry_commands:
      - "/emergency"
    emergency_types:
      - power_outage
      - equipment_failure
      - customer_complaint

tools:
  wecom_api:
    enabled: true
    base_url: "https://qyapi.weixin.qq.com/cgi-bin"
    
  wps_api:
    enabled: true
    base_url: "https://openapi.wps.cn"
    app_id: "${WPS_APP_ID}"
    app_secret: "${WPS_APP_SECRET}"
    
  baidu_stt:
    enabled: true
    api_key: "${BAIDU_API_KEY}"
    secret_key: "${BAIDU_SECRET_KEY}"
    
  paddle_ocr:
    enabled: true
    mode: online  # or local
    
session:
  storage: redis
  timeout: 3600  # 1小时
  persistence: true

notification:
  daily_report:
    enabled: true
    schedule: "0 18 * * *"
    
  weekly_report:
    enabled: true
    schedule: "0 18 * * 5"
```

### 3.3 Skills详细设计

#### 3.3.1 StationWorkGuide Skill

```yaml
skill_id: station_work_guide
name: 驻点工作引导
description: 引导现场人员完成驻点工作的全流程采集

states:
  - IDLE: 等待启动
  - PREPARATION: 准备阶段（查询历史、生成清单）
  - COLLECTION: 采集阶段（分项采集）
  - REVIEW: 审核阶段（完整性检查）
  - COMPLETED: 完成

workflow:
  preparation:
    steps:
      - query_community_info:
          tool: wps_api
          action: query_records
          table: "小区信息"
          filter: "小区名称 = {community_name}"
      
      - query_history:
          tool: wps_api
          action: query_records
          table: "驻点记录"
          filter: "小区ID = {community_id} ORDER BY 驻点日期 DESC LIMIT 1"
      
      - generate_task_list:
          template: "驻点任务清单"
          context: [community_info, history_record]
    
    output:
      - 小区基础信息
      - 上次驻点日期
      - 待处理事项
      - 本次任务清单

  collection:
    phases:
      power_room:
        name: 配电房信息采集
        steps:
          - guide_to_location:
              message: "请前往{配电房名称}，位置：{位置描述}"
              action: wait_for_user_response
          
          - capture_entrance_photo:
              message: "请拍摄配电房入口照片"
              action: receive_image
              validation: image_quality_check
          
          - record_location_description:
              message: "请描述配电房具体位置"
              action: receive_voice
              tool: baidu_stt
          
          - capture_equipment_photos:
              message: "请拍摄变压器铭牌照片"
              action: receive_image
              tool: paddle_ocr
              extract: [型号, 容量, 厂家]
          
          - record_equipment_status:
              message: "请描述设备运行状态"
              action: receive_voice
              tool: [baidu_stt, nlp_extract]
          
          - check_for_defects:
              message: "是否有设备缺陷或隐患？"
              action: receive_choice
              options: ["无", "有"]
              if: "有"
              then:
                - capture_defect_photo
                - record_defect_description
                - classify_defect_level
        
        storage:
          tool: wps_api
          action: insert_record
          table: "配电房信息"
      
      customer_visit:
        name: 客户走访
        steps:
          - recommend_customers:
              tool: wps_api
              action: query_records
              query: |
                SELECT * FROM 客户信息 
                WHERE 小区ID = {community_id} 
                AND (敏感客户 = true OR 上次走访 < DATE_SUB(NOW(), INTERVAL 3 MONTH))
          
          - select_customer:
              message: "请选择要走访的客户"
              action: present_options
              options: "{recommended_customers}"
          
          - record_visit:
              steps:
                - record_feedback:
                    message: "请记录客户反馈"
                    action: receive_voice
                    tool: baidu_stt
                
                - classify_issue:
                    message: "问题类型？"
                    action: receive_choice
                    options: ["无", "停电", "电费", "服务态度", "其他"]
                
                - record_satisfaction:
                    message: "客户满意度？"
                    action: receive_choice
                    options: ["非常满意", "满意", "一般", "不满意"]
                
                - mark_follow_up:
                    message: "是否需要回访？"
                    action: receive_choice
                    options: ["是", "否"]
        
        storage:
          tool: wps_api
          action: insert_record
          table: "走访记录"
      
      emergency_info:
        name: 应急信息采集
        steps:
          - capture_entry_point:
              message: "请拍摄发电车进入点照片"
              action: receive_image
          
          - capture_parking_point:
              message: "请拍摄停放点照片"
              action: receive_image
          
          - capture_access_point:
              message: "请拍摄接入点照片"
              action: receive_image
          
          - record_cable_info:
              message: "请记录电缆型号和长度"
              action: receive_voice
              tool: [baidu_stt, nlp_extract]
              extract: [电缆型号, 电缆长度]
        
        storage:
          tool: wps_api
          action: update_record
          table: "应急接入信息"

  review:
    checks:
      - photo_quality:
          criteria: "清晰度 > 0.7"
          action: flag_if_poor
      
      - data_completeness:
          criteria: "必填字段100%填充"
          action: list_missing_fields
      
      - logic_validation:
          criteria: "数值范围合理，日期格式正确"
          action: flag_invalid_data
    
    output:
      - 审核报告
      - 缺失项清单
      - 建议补充内容

  completion:
    actions:
      - trigger_doc_generation:
          skill: auto_doc_generation
          docs: [power_briefing, work_summary]
      
      - send_notification:
          type: work_completed
          receivers: [user, supervisor]
      
      - update_knowledge_base:
          tool: wps_api
          action: update_records
```

#### 3.3.2 AutoDocGeneration Skill

```yaml
skill_id: auto_doc_generation
name: 文档自动生成
description: 基于采集数据自动生成标准化业务文档

document_templates:
  power_briefing:
    name: 小区供电简报
    template_file: "tpl_power_briefing.docx"
    data_sources:
      - table: "小区信息"
        fields: [小区名称, 地址, 户数, 配电房数, 变压器数]
      
      - table: "配电房信息"
        filter: "小区ID = {community_id}"
        fields: [配电房名称, 变压器数量, 设备状态]
      
      - table: "走访记录"
        filter: "小区ID = {community_id} AND 走访日期 >= {last_month}"
        aggregation: 
          - count(记录ID) AS 走访次数
          - avg(满意度) AS 平均满意度
    
    sections:
      - title: "小区基本信息"
        content: "{小区名称}位于{地址}，共有{户数}户居民，配备{配电房数}个配电房，{变压器数}台变压器。"
      
      - title: "供电设施概况"
        table: "{配电房信息}"
      
      - title: "客户服务情况"
        content: "近一个月走访{走访次数}户，平均满意度{平均满意度}。"
      
      - title: "近期工作计划"
        content: "基于采集数据智能生成"
    
    output:
      filename: "{小区名称}_供电简报_{日期}.docx"
      location: "/{供电所}/{小区名称}/供电简报/"
      format: [docx, pdf]

  emergency_guide:
    name: 应急发电指引
    template_file: "tpl_emergency_guide.docx"
    data_sources:
      - table: "应急接入信息"
        filter: "小区ID = {community_id}"
        fields: [进入点描述, 停放点描述, 接入点描述, 电缆型号, 电缆长度]
      
      - table: "小区信息"
        fields: [物业联系人, 物业电话]
    
    sections:
      - title: "小区位置及入口"
        images: [进入点照片]
        content: "{进入点描述}"
      
      - title: "发电车停放点"
        images: [停放点照片]
        content: "{停放点描述}"
      
      - title: "接入点位置"
        images: [接入点照片]
        content: "{接入点描述}"
      
      - title: "电缆信息"
        content: "型号：{电缆型号}，长度：{电缆长度}米"
      
      - title: "物业联系人"
        content: "{物业联系人} {物业电话}"
      
      - title: "安全注意事项"
        content: "标准安全规范"
    
    output:
      filename: "{小区名称}_应急发电指引.docx"
      location: "/{供电所}/{小区名称}/"
      format: docx

  work_summary:
    name: 驻点工作总结
    template_file: "tpl_work_summary.docx"
    data_sources:
      - table: "驻点记录"
        filter: "记录ID = {record_id}"
      
      - table: "配电房信息"
        filter: "本次采集的配电房ID列表"
      
      - table: "走访记录"
        filter: "本次走访的记录ID列表"
    
    sections:
      - title: "工作概况"
        content: "本次驻点工作完成情况"
      
      - title: "配电房检查情况"
        table: "配电房信息汇总"
      
      - title: "客户走访情况"
        table: "走访记录汇总"
      
      - title: "发现问题及处理"
        content: "缺陷和隐患清单"
      
      - title: "后续工作计划"
        content: "基于问题清单生成"
    
    output:
      filename: "{小区名称}_驻点工作总结_{日期}.docx"
      location: "/{供电所}/{小区名称}/驻点工作/"
      format: docx

workflow:
  1_fetch_data:
    description: 从WPS多维表格查询数据
    tool: wps_api
    action: query_records
    parallel: true
  
  2_process_data:
    description: 数据格式化和计算
    actions:
      - format_dates
      - calculate_statistics
      - generate_charts_if_needed
  
  3_fill_template:
    description: 填充文档模板
    tool: wps_api
    action: generate_document
    params:
      template_id: "{doc_type}"
      data: "{processed_data}"
  
  4_save_document:
    description: 保存到WPS云文档
    tool: wps_api
    action: save_file
    params:
      folder: "{location}"
      share_with: ["供电所群组"]
  
  5_notify_user:
    description: 通知用户文档已生成
    channel: wecom
    message: "{文档类型}已生成：{文档链接}"
```

#### 3.3.3 EmergencyGuide Skill

```yaml
skill_id: emergency_guide
name: 应急处置指引
description: 在应急情况下快速响应，提供处置指引和资源支持

triggers:
  commands:
    - "/emergency {type} {location}"
    - keywords: ["停电", "故障", "抢修", "应急"]
  
emergency_types:
  power_outage:
    name: 停电故障
    priority: high
    workflow:
      - step_1_confirm_scope:
          action: ask_user
          question: "请确认停电影响范围"
          options: ["单户", "整栋楼", "整个小区", "不确定"]
      
      - step_2_query_sensitive_customers:
          tool: wps_api
          action: query_records
          query: |
            SELECT * FROM 客户信息 
            WHERE 小区ID = {community_id} 
            AND 敏感客户 = true
          
          if_results: 
            action: urgent_notification
            message: "⚠️ 发现{count}户敏感客户，请立即联系！"
            send_to: [user, supervisor]
      
      - step_3_fetch_emergency_plan:
          tool: wps_api
          action: get_document
          doc_path: "/{供电所}/{小区名}/应急发电指引.docx"
          
          action: send_card_message
          title: "应急发电指引"
          content: "点击查看详细指引"
          buttons:
            - text: "查看指引"
              url: "{doc_url}"
            - text: "导航到接入点"
              type: navigation
      
      - step_4_guided_response:
          steps:
            - "立即联系物业确认情况（联系人：{物业联系人} {物业电话}）"
            - "安抚敏感客户（清单已推送）"
            - "准备应急发电车（按指引操作）"
            - "拍摄现场照片记录"
            - "每30分钟更新进展"
      
      - step_5_record_progress:
          loop: every_30_minutes
          until: resolved
          actions:
            - prompt_user: "请更新处理进展"
            - record_timestamp
            - capture_photos
          
          on_resolve:
            - generate_emergency_report
            - notify_completion

  equipment_failure:
    name: 设备故障
    priority: high
    workflow:
      - step_1_identify_equipment:
          action: receive_user_input
          question: "请描述故障设备信息"
          photo_required: true
      
      - step_2_query_equipment_info:
          tool: wps_api
          action: query_records
          table: "配电房信息"
          filter: "设备标识匹配"
      
      - step_3_safety_checklist:
          checklist:
            - "是否已断电？"
            - "是否设置警示标识？"
            - "是否通知相关人员？"
          
          all_required: true
      
      - step_4_guide_repair:
          steps:
            - "记录故障现象（拍照）"
            - "联系抢修队伍（推荐：{抢修队联系人}）"
            - "准备备件（参考设备信息：{设备型号}）"
            - "监督抢修过程"
            - "验收并记录"

notification_rules:
  on_trigger:
    receivers: [user, supervisor]
    priority: urgent
    
  on_sensitive_customer_found:
    receivers: [user, supervisor, customer_service]
    priority: urgent
    
  on_progress_update:
    receivers: [supervisor]
    frequency: every_30_minutes
    
  on_resolve:
    receivers: [user, supervisor, relevant_parties]
    message: "应急事件已处理完成"
```

### 3.4 Tools设计

#### 3.4.1 企业微信API Tool

```typescript
// tools/wecom-api.tool.ts
interface WeComAPITool {
  name: 'wecom_api';
  version: '1.0.0';
  
  methods: {
    // 发送文本消息
    sendTextMessage(params: {
      user_id: string;
      content: string;
    }): Promise<MessageResult>;
    
    // 发送Markdown消息
    sendMarkdownMessage(params: {
      user_id: string;
      markdown: string;
    }): Promise<MessageResult>;
    
    // 发送图文卡片
    sendCardMessage(params: {
      user_id: string;
      title: string;
      description: string;
      url: string;
      buttons?: Array<{
        text: string;
        url?: string;
        type?: 'navigation' | 'link';
      }>;
    }): Promise<MessageResult>;
    
    // 发送图片
    sendImageMessage(params: {
      user_id: string;
      image_url: string;
    }): Promise<MessageResult>;
    
    // 接收消息解析
    parseIncomingMessage(payload: WebhookPayload): ParsedMessage;
    
    // 上传临时素材
    uploadMedia(params: {
      type: 'image' | 'voice' | 'video' | 'file';
      file_path: string;
    }): Promise<MediaResult>;
    
    // 获取用户信息
    getUserInfo(user_id: string): Promise<UserInfo>;
    
    // 发送群消息
    sendGroupMessage(params: {
      chat_id: string;
      msg_type: string;
      content: any;
    }): Promise<MessageResult>;
  };
}
```

#### 3.4.2 WPS API Tool

```typescript
// tools/wps-api.tool.ts
interface WPSAPITool {
  name: 'wps_api';
  version: '1.0.0';
  
  config: {
    app_id: string;
    app_secret: string;
    base_url: 'https://openapi.wps.cn';
  };
  
  methods: {
    // 获取access_token
    getAccessToken(): Promise<string>;
    
    // ========== 多维表格操作 ==========
    
    // 查询记录
    queryRecords(params: {
      file_id: string;
      sheet_id?: string;
      filter?: FilterCondition;
      sort?: SortCondition;
      limit?: number;
      offset?: number;
    }): Promise<QueryResult>;
    
    // 添加记录
    insertRecord(params: {
      file_id: string;
      sheet_id?: string;
      record: RecordData;
    }): Promise<InsertResult>;
    
    // 批量添加记录
    insertRecords(params: {
      file_id: string;
      sheet_id?: string;
      records: RecordData[];
    }): Promise<InsertResult>;
    
    // 更新记录
    updateRecord(params: {
      file_id: string;
      record_id: string;
      record: Partial<RecordData>;
    }): Promise<UpdateResult>;
    
    // 删除记录
    deleteRecord(params: {
      file_id: string;
      record_id: string;
    }): Promise<DeleteResult>;
    
    // 获取表格结构
    getSheetSchema(params: {
      file_id: string;
      sheet_id?: string;
    }): Promise<SchemaResult>;
    
    // ========== 文档操作 ==========
    
    // 创建文档
    createDocument(params: {
      type: 'docx' | 'xlsx' | 'pptx';
      name: string;
      folder_id?: string;
    }): Promise<CreateDocResult>;
    
    // 获取文档内容
    getDocumentContent(params: {
      file_id: string;
    }): Promise<DocContent>;
    
    // 生成文档（基于模板）
    generateDocument(params: {
      template_id: string;
      data: object;
      output_name: string;
      output_format?: 'docx' | 'pdf';
    }): Promise<GenerateResult>;
    
    // 保存文件到指定位置
    saveFile(params: {
      file_id: string;
      folder_id: string;
      new_name?: string;
    }): Promise<SaveResult>;
    
    // 获取分享链接
    getShareLink(params: {
      file_id: string;
      permission?: 'read' | 'write';
      expire_days?: number;
    }): Promise<ShareResult>;
    
    // ========== 文件夹操作 ==========
    
    // 创建文件夹
    createFolder(params: {
      name: string;
      parent_id?: string;
    }): Promise<FolderResult>;
    
    // 列出文件夹内容
    listFolder(params: {
      folder_id: string;
    }): Promise<ListResult>;
  };
}
```

#### 3.4.3 百度语音识别 Tool

```typescript
// tools/baidu-stt.tool.ts
interface BaiduSTTTool {
  name: 'baidu_stt';
  version: '1.0.0';
  
  config: {
    api_key: string;
    secret_key: string;
    dev_pid: 1537; // 普通话
  };
  
  methods: {
    // 语音识别
    recognize(params: {
      audio_url: string;
      format?: 'pcm' | 'wav' | 'amr';
      rate?: 16000;
    }): Promise<RecognitionResult>;
    
    // 语音转文字（实时）
    realTimeRecognize(stream: AudioStream): AsyncIterator<RecognitionChunk>;
  };
}

interface RecognitionResult {
  text: string;
  confidence: number;
  err_no: number;
  err_msg: string;
}
```

#### 3.4.4 OCR识别 Tool

```typescript
// tools/paddle-ocr.tool.ts
interface PaddleOCRTool {
  name: 'paddle_ocr';
  version: '1.0.0';
  
  config: {
    mode: 'online' | 'local';
    api_endpoint?: string;
  };
  
  methods: {
    // 通用文字识别
    recognizeText(params: {
      image_url: string;
    }): Promise<OCRResult>;
    
    // 结构化识别（铭牌、发票等）
    recognizeStructured(params: {
      image_url: string;
      template_type: 'nameplate' | 'invoice' | 'idcard';
    }): Promise<StructuredResult>;
  };
}

interface OCRResult {
  texts: Array<{
    content: string;
    confidence: number;
    position: [number, number, number, number];
  }>;
}

interface StructuredResult {
  fields: Record<string, string>;
  confidence: number;
}
```

---

## 四、数据模型设计

### 4.1 WPS多维表格设计

```yaml
# 表1: 供电所配置表
table: power_station_config
description: 供电所基础配置信息
columns:
  - station_id: string (主键)  # 供电所唯一ID
  - station_name: string       # 供电所名称
  - wecom_corp_id: string      # 企业微信企业ID
  - wecom_agent_id: string     # 企业微信应用ID
  - wps_root_folder_id: string # WPS根文件夹ID
  - work_group_chat_id: string # 工作群ID
  - supervisor_user_id: string # 所长企业微信UserID
  - created_at: datetime
  - updated_at: datetime

# 表2: 小区信息表
table: community_info
description: 小区基础信息
columns:
  - community_id: string (主键)
  - station_id: string (外键，供电所ID)
  - community_name: string     # 小区名称
  - address: string            # 详细地址
  - total_households: number   # 总户数
  - power_room_count: number   # 配电房数量
  - transformer_count: number  # 变压器数量
  - property_company: string   # 物业公司名称
  - property_contact: string   # 物业联系人
  - property_phone: string     # 物业电话
  - sensitive_customer_count: number  # 敏感客户数
  - last_station_date: date    # 上次驻点日期
  - station_count: number      # 累计驻点次数
  - created_at: datetime
  - updated_at: datetime

# 表3: 驻点工作记录表
table: station_work_records
description: 驻点工作记录
columns:
  - record_id: string (主键)
  - station_id: string (外键)
  - community_id: string (外键)
  - work_date: date            # 驻点日期
  - worker_user_id: string     # 客户经理UserID
  - worker_name: string        # 客户经理姓名
  - work_summary: text         # 工作内容摘要
  - power_room_checked: boolean  # 是否检查配电房
  - customer_visit_count: number # 走访客户数
  - issue_found_count: number    # 发现问题数
  - issue_resolved_count: number # 解决问题数
  - photo_count: number        # 照片数量
  - status: enum               # 状态：进行中/已完成/已审核
    values: [in_progress, completed, reviewed]
  - related_doc_urls: array    # 关联文档链接列表
  - created_at: datetime
  - updated_at: datetime

# 表4: 配电房信息表
table: power_room_info
description: 配电房详细信息
columns:
  - room_id: string (主键)
  - station_id: string (外键)
  - community_id: string (外键)
  - room_name: string          # 配电房名称
  - location_description: text # 位置描述
  - photo_urls: array          # 照片URL列表
  - transformer_count: number  # 变压器数量
  - equipment_status: enum     # 设备状态
    values: [normal, abnormal, under_repair]
  - defect_description: text   # 缺陷描述
  - last_check_date: date      # 上次检查日期
  - check_records: json        # 检查记录（JSON格式）
  - created_at: datetime
  - updated_at: datetime

# 表5: 变压器信息表
table: transformer_info
description: 变压器设备信息
columns:
  - transformer_id: string (主键)
  - room_id: string (外键，配电房ID)
  - station_id: string (外键)
  - model: string              # 型号
  - capacity: number           # 容量（kVA）
  - manufacturer: string       # 制造商
  - install_date: date         # 投运日期
  - photo_urls: array          # 照片
  - status: enum               # 运行状态
    values: [normal, abnormal, stopped]
  - last_maintenance_date: date # 上次检修日期
  - created_at: datetime
  - updated_at: datetime

# 表6: 应急接入信息表
table: emergency_access_info
description: 应急发电车接入信息
columns:
  - community_id: string (主键)
  - station_id: string (外键)
  - entry_point_description: text    # 进入点描述
  - entry_point_photos: array        # 进入点照片
  - parking_point_description: text  # 停放点描述
  - parking_point_photos: array      # 停放点照片
  - access_point_description: text   # 接入点描述
  - access_point_photos: array       # 接入点照片
  - cable_model: string              # 电缆型号
  - cable_length: number             # 电缆长度（米）
  - access_conditions: text          # 接入条件说明
  - emergency_contact: string        # 应急联系人
  - emergency_phone: string          # 应急电话
  - updated_at: datetime

# 表7: 客户信息表
table: customer_info
description: 小区客户信息
columns:
  - customer_id: string (主键)
  - community_id: string (外键)
  - station_id: string (外键)
  - address: string              # 详细地址（如：2-3-501）
  - is_sensitive: boolean       # 是否敏感客户
  - sensitive_type: enum         # 敏感类型
    values: [elderly, pregnant, baby, medical_equipment, other]
  - contact_phone: string        # 联系电话
  - last_visit_date: date        # 上次走访日期
  - complaint_count: number      # 投诉次数
  - notes: text                  # 备注
  - created_at: datetime
  - updated_at: datetime

# 表8: 客户走访记录表
table: customer_visit_records
description: 客户走访记录
columns:
  - visit_id: string (主键)
  - station_id: string (外键)
  - community_id: string (外键)
  - customer_id: string (外键)
  - visit_date: date             # 走访日期
  - worker_user_id: string       # 走访人UserID
  - worker_name: string          # 走访人姓名
  - visit_content: text          # 走访内容记录
  - issue_type: enum             # 问题类型
    values: [none, power_outage, electricity_fee, service, other]
  - issue_description: text      # 问题描述
  - resolution: text             # 处理措施
  - satisfaction: enum           # 满意度
    values: [very_satisfied, satisfied, neutral, dissatisfied]
  - need_follow_up: boolean      # 是否需要回访
  - follow_up_date: date         # 计划回访日期
  - photo_urls: array            # 现场照片
  - created_at: datetime

# 表9: 设备缺陷记录表
table: equipment_defect_records
description: 设备缺陷和隐患记录
columns:
  - defect_id: string (主键)
  - station_id: string (外键)
  - room_id: string (外键)      # 关联配电房
  - transformer_id: string (外键,可选) # 关联变压器
  - defect_type: enum            # 缺陷类型
    values: [equipment_aging, line_damage, environment, safety, other]
  - severity: enum               # 严重程度
    values: [critical, major, minor]
  - description: text            # 详细描述
  - photo_urls: array            # 照片
  - discovered_date: date        # 发现日期
  - discovered_by: string        # 发现人
  - status: enum                 # 处理状态
    values: [pending, processing, resolved, closed]
  - resolution: text             # 处理结果
  - resolved_date: date          # 解决日期
  - created_at: datetime
  - updated_at: datetime

# 表10: 通知记录表
table: notification_records
description: 通知发送记录
columns:
  - notification_id: string (主键)
  - station_id: string (外键)
  - notification_type: string    # 通知类型
  - sender: string               # 发送者
  - receivers: array             # 接收人列表
  - content: text                # 通知内容
  - related_record_id: string    # 关联记录ID
  - priority: enum               # 优先级
    values: [low, normal, high, urgent]
  - status: enum                 # 发送状态
    values: [pending, sent, failed]
  - read_status: json            # 阅读状态（用户ID:时间）
  - created_at: datetime
```

### 4.2 权限控制实现

```javascript
// 权限中间件
class PermissionMiddleware {
  // 获取当前用户所属供电所
  async getUserPowerStation(userId) {
    const userInfo = await wecomApi.getUserInfo(userId);
    return userInfo.extattr.power_station_id;
  }
  
  // 查询权限过滤
  async filterQueryByPermission(query, userId) {
    const stationId = await this.getUserPowerStation(userId);
    
    // 自动添加供电所过滤条件
    return {
      ...query,
      station_id: {
        operator: 'equals',
        value: stationId
      }
    };
  }
  
  // 写入权限检查
  async checkWritePermission(recordId, userId) {
    const record = await wpsApi.getRecord(recordId);
    const userStation = await this.getUserPowerStation(userId);
    
    if (record.station_id !== userStation) {
      throw new Error('无权操作其他供电所的数据');
    }
    
    return true;
  }
  
  // 文档访问权限检查
  async checkDocAccess(docUrl, userId) {
    const userStation = await this.getUserPowerStation(userId);
    const docStation = this.extractStationFromUrl(docUrl);
    
    if (userStation !== docStation) {
      return { allowed: false, reason: '无权访问其他供电所的文档' };
    }
    
    return { allowed: true };
  }
}
```

---

## 五、接口设计

### 5.1 企业微信消息接口

```yaml
# 接收消息回调
endpoint: POST /webhook/wecom
description: 接收企业微信推送的用户消息和事件

request:
  headers:
    Content-Type: application/xml
  body:
    ToUserName: string      # 企业微信CorpID
    FromUserName: string    # 发送者UserID
    CreateTime: number      # 消息创建时间
    MsgType: string         # 消息类型：text/image/voice/location/event
    Content: string         # 文本消息内容
    PicUrl: string          # 图片URL
    MediaId: string         # 媒体文件ID
    Format: string          # 语音格式
    Recognition: string     # 语音识别结果（需开通）
    Event: string           # 事件类型
    EventKey: string        # 事件KEY值

response:
  content_type: application/xml
  body: |
    <xml>
      <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
      <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
      <CreateTime>{timestamp}</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[{reply_content}]]></Content>
    </xml>

# 发送应用消息
endpoint: POST /cgi-bin/message/send
headers:
  Authorization: Bearer {access_token}

request_body:
  touser: string           # 接收人UserID
  msgtype: string          # 消息类型
  text:
    content: string        # 文本内容
  markdown:
    content: string        # Markdown内容
  template_card:           # 模板卡片
    card_type: string
    source:
      desc: string
    main_title:
      title: string
      desc: string
    jump_list:
      - type: number
        url: string
        title: string
    card_action:
      type: number
      url: string
```

### 5.2 WPS开放平台接口

```yaml
# 查询多维表格记录
endpoint: POST /kopen/office/file/{file_id}/core/execute/db/query
headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json

request_body:
  sheetId: string          # 工作表ID
  criteria:                # 筛选条件
    - field: string        # 字段名
      operator: string     # 操作符：equals/contains/gt/lt等
      value: any           # 值
  sort:                    # 排序
    - field: string
      order: asc/desc
  limit: number            # 返回数量
  offset: number           # 偏移量

response:
  records:
    - recordId: string
      fields:
        field_name: value
  total: number
  nextOffset: number

# 添加记录
endpoint: POST /kopen/office/file/{file_id}/core/execute/db/insert
request_body:
  sheetId: string
  records:
    - fields:
        field_name: value

# 更新记录
endpoint: POST /kopen/office/file/{file_id}/core/execute/db/update
request_body:
  sheetId: string
  recordId: string
  fields:
    field_name: value

# 基于模板生成文档
endpoint: POST /kopen/api/v1/doc/generate
request_body:
  template_id: string      # 模板文件ID
  data: object             # 填充数据
  output_name: string      # 输出文件名
  output_format: docx/pdf  # 输出格式
```

---

## 六、部署方案

### 6.1 部署架构

```yaml
# docker-compose.yaml
version: '3.8'

services:
  # OpenClaw Gateway
  openclaw-gateway:
    image: openclaw/gateway:latest
    container_name: field-info-agent
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - REDIS_URL=redis://redis:6379
      # 企业微信配置
      - WECOM_CORP_ID=${WECOM_CORP_ID}
      - WECOM_AGENT_ID=${WECOM_AGENT_ID}
      - WECOM_SECRET=${WECOM_SECRET}
      - WECOM_TOKEN=${WECOM_TOKEN}
      - WECOM_AES_KEY=${WECOM_AES_KEY}
      # WPS配置
      - WPS_APP_ID=${WPS_APP_ID}
      - WPS_APP_SECRET=${WPS_APP_SECRET}
      # 百度语音
      - BAIDU_API_KEY=${BAIDU_API_KEY}
      - BAIDU_SECRET_KEY=${BAIDU_SECRET_KEY}
    volumes:
      - ./config:/app/config
      - ./skills:/app/skills
      - ./logs:/app/logs
    depends_on:
      - redis
    restart: always
    networks:
      - agent-network

  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: agent-redis
    volumes:
      - redis_data:/data
    restart: always
    networks:
      - agent-network

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    container_name: agent-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - openclaw-gateway
    restart: always
    networks:
      - agent-network

volumes:
  redis_data:

networks:
  agent-network:
    driver: bridge
```

### 6.2 环境配置

```yaml
# .env.example
# 企业微信配置
WECOM_CORP_ID=wwxxxxxxxxxxxxxxxx
WECOM_AGENT_ID=1000002
WECOM_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WECOM_TOKEN=xxxxxxxxxxxx
WECOM_AES_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# WPS开放平台配置
WPS_APP_ID=xxxxxxxxxxxxxxxx
WPS_APP_SECRET=xxxxxxxxxxxxxxxx

# 百度语音配置
BAIDU_API_KEY=xxxxxxxxxxxxxxxx
BAIDU_SECRET_KEY=xxxxxxxxxxxxxxxx

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# 日志级别
LOG_LEVEL=info

# 会话超时时间（秒）
SESSION_TIMEOUT=3600
```

---

## 七、实施路线图

### 7.1 阶段规划

```yaml
phases:
  phase_1_setup: # 第1-2周
    name: 基础环境搭建
    tasks:
      - task: 申请API权限
        details:
          - WPS开放平台账号申请
          - 多维表格API权限申请
          - 文档API权限申请
          - 企业微信自建应用创建
      
      - task: 部署开发环境
        details:
          - 云服务器准备
          - Docker环境安装
          - OpenClaw Gateway部署
          - Redis部署
      
      - task: 配置企业微信
        details:
          - 创建自建应用
          - 配置回调URL
          - 设置消息加解密
          - 申请所需API权限
    
    deliverables:
      - 可运行的开发环境
      - 企业微信应用可接收消息
      - WPS API可正常调用

  phase_2_core: # 第3-5周
    name: 核心功能开发
    tasks:
      - task: 开发StationWorkGuide Skill
        details:
          - 实现工作启动流程
          - 实现配电房信息采集
          - 实现客户走访记录
          - 实现应急信息采集
          - 实现智能审核功能
      
      - task: 开发WPS API Tool
        details:
          - 实现多维表格CRUD
          - 实现文档生成
          - 实现文件存储
      
      - task: 开发企业微信API Tool
        details:
          - 实现消息发送
          - 实现消息解析
          - 实现素材上传
      
      - task: 集成语音识别
        details:
          - 集成百度语音API
          - 实现语音转文字
          - 实现关键词提取
    
    deliverables:
      - 完整的驻点工作采集流程
      - 数据可正常存储到WPS
      - 可通过企业微信交互

  phase_3_docs: # 第6-7周
    name: 文档生成与通知
    tasks:
      - task: 开发AutoDocGeneration Skill
        details:
          - 开发供电简报模板
          - 开发应急发电指引模板
          - 开发驻点工作总结模板
          - 实现文档自动填充
          - 实现文档自动保存
      
      - task: 开发通知系统
        details:
          - 实现工作完成通知
          - 实现问题发现通知
          - 实现日报/周报定时任务
          - 实现应急事件通知
      
      - task: 创建文档模板
        details:
          - 设计Word模板
          - 配置模板字段映射
          - 上传模板到WPS
    
    deliverables:
      - 可自动生成各类文档
      - 通知系统正常运行
      - 定时任务配置完成

  phase_4_emergency: # 第8周
    name: 应急处置功能
    tasks:
      - task: 开发EmergencyGuide Skill
        details:
          - 实现应急事件启动
          - 实现敏感客户查询
          - 实现应急方案推送
          - 实现过程记录
          - 实现应急报告生成
    
    deliverables:
      - 应急处置流程可用
      - 可正常查询敏感客户
      - 应急报告可自动生成

  phase_5_pilot: # 第9-12周
    name: 试点验证
    tasks:
      - task: 选择试点供电所
        details:
          - 确定试点单位
          - 收集现有工作模式
          - 准备试点数据
      
      - task: 培训现场人员
        details:
          - 编写操作手册
          - 开展培训课程
          - 提供技术支持
      
      - task: 试点运行
        details:
          - 正式启用系统
          - 收集用户反馈
          - 记录问题和建议
      
      - task: 优化迭代
        details:
          - 修复发现的问题
          - 优化用户体验
          - 完善功能细节
    
    deliverables:
      - 试点运行报告
      - 优化后的系统
      - 完整的操作文档

  phase_6_rollout: # 第13周及以后
    name: 全面推广
    tasks:
      - task: 逐步推广到其他供电所
      - task: 建立运维支持体系
      - task: 持续优化和升级
```

### 7.2 里程碑

| 里程碑 | 时间 | 交付物 | 验收标准 |
|--------|------|--------|----------|
| M1 | Week 2 | 基础环境就绪 | 可接收企业微信消息，可调用WPS API |
| M2 | Week 5 | 核心采集功能 | 可完成一次完整的驻点工作采集 |
| M3 | Week 7 | 文档自动生成 | 可自动生成3类文档并保存到WPS |
| M4 | Week 8 | 应急处置功能 | 可完成应急事件全流程处理 |
| M5 | Week 12 | 试点完成 | 试点供电所正常使用，反馈良好 |
| M6 | Week 13+ | 全面推广 | 所有供电所接入使用 |

---

## 八、风险与应对

### 8.1 技术风险

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|----------|
| WPS API调用频率限制 | 中 | 高 | 实现请求队列和重试机制；申请提高限额 |
| 企业微信消息延迟 | 中 | 中 | 优化消息处理逻辑；设置超时机制 |
| 语音识别准确率不足 | 中 | 中 | 结合上下文理解；提供人工校正入口 |
| OCR识别失败 | 低 | 中 | 提示用户手动输入；记录失败案例优化 |

### 8.2 业务风险

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|----------|
| 现场人员接受度低 | 中 | 高 | 充分培训；简化操作流程；提供人工支持 |
| 网络覆盖不足 | 中 | 高 | 提前告知网络要求；优化使用体验 |
| 数据安全问题 | 低 | 高 | 加密传输；权限控制；审计日志 |

---

## 九、附录

### 9.1 术语表

| 术语 | 说明 |
|------|------|
| OpenClaw | AI助手框架，提供Agent、Skill、Tool架构 |
| Skill | 业务技能，封装特定业务场景的能力 |
| Tool | 工具，对接外部API或本地服务 |
| Channel | 消息渠道，如企业微信、钉钉等 |
| WPS多维表格 | WPS的在线数据库产品，类似Airtable |
| 驻点工作 | 供电所人员到小区现场开展的工作 |
| 敏感客户 | 需要特别关怀的客户（老人、孕妇等） |

### 9.2 参考文档

- [企业微信开发者文档](https://developer.work.weixin.qq.com/document)
- [WPS开放平台文档](https://open.wps.cn/docs)
- [OpenClaw架构文档](https://github.com/cline/cline)
- [百度语音识别API](https://ai.baidu.com/tech/speech)

---

**文档结束**

**备注**: 本PRD基于SEARCH-R方法论完成，已充分考虑企业微信、WPS开放平台、OpenClaw的技术能力和限制。