# 现场信息收集Agent - 架构设计方案

## 一、整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ 企业微信APP  │  │ 手机拍照    │  │ 语音输入            │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          └────────────────┴────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                  企业微信平台层                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  自建应用 / 群聊机器人                                  │ │
│  │  - 接收消息（文字、语音、图片）                         │ │
│  │  - 推送消息（文字、卡片、文档链接）                     │ │
│  └──────────────────────┬─────────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────────┘
                          │ 企业微信回调/API
┌─────────────────────────▼───────────────────────────────────┐
│                  OpenClaw Agent层（云端）                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  OpenClaw Gateway                                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐   │ │
│  │  │ Channel     │  │ Session     │  │ Skills        │   │ │
│  │  │ - WeCom     │  │ Manager     │  │ - InfoCollect │   │ │
│  │  │   Provider  │  │             │  │ - DocGenerate │   │ │
│  │  │             │  │             │  │ - GuideAssist │   │ │
│  │  └─────────────┘  └─────────────┘  └───────────────┘   │ │
│  └──────────────────────┬─────────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────────┘
                          │ HTTPS/API
┌─────────────────────────▼───────────────────────────────────┐
│                     外部服务层                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ 百度语音API   │  │ WPS开放平台   │  │ 本地AI模型       │  │
│  │ - 语音识别   │  │ - 多维表格    │  │ - 信息抽取       │  │
│  │ - 方言支持   │  │ - 文档生成    │  │ - 内容审核       │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、核心组件设计

### 2.1 OpenClaw Channel配置（企业微信）

```yaml
# openclaw.config.yaml
channels:
  wecom:
    enabled: true
    type: official  # 使用企业微信官方API
    
    # 企业微信应用配置
    corp_id: "${WECOM_CORP_ID}"
    agent_id: "${WECOM_AGENT_ID}"
    secret: "${WECOM_SECRET}"
    
    # 消息接收配置
    callback:
      url: "https://your-agent-domain.com/webhook/wecom"
      token: "${WECOM_TOKEN}"
      encoding_aes_key: "${WECOM_AES_KEY}"
    
    # 功能开关
    features:
      text_message: true      # 文字消息
      voice_message: true     # 语音消息
      image_message: true     # 图片消息
      file_message: true      # 文件消息
      location_message: true  # 位置信息
      
    # 会话管理
    session:
      timeout: 3600  # 1小时无操作结束会话
      persistence: true  # 持久化会话
```

### 2.2 Skills设计（核心能力）

#### Skill 1: 驻点工作引导（StationWorkGuide）

```yaml
skill_id: station_work_guide
name: 驻点工作引导
description: 引导现场人员完成驻点工作的全流程

triggers:
  - command: "/start-station-work"
  - keyword: ["开始驻点", "驻点工作", "现场采集"]
  - intent: "开始驻点任务"

workflow:
  phase_1_preparation:  # 阶段1：提前准备
    - query_community_info:      # 查询小区信息
        tool: wps_ksheet_query
        params:
          table: "小区基础信息表"
          filter: "小区名称 = {community_name}"
    
    - check_history_records:     # 检查历史记录
        tool: wps_ksheet_query
        params:
          table: "驻点工作记录"
          filter: "小区 = {community_name} AND 日期 >= {last_month}"
    
    - generate_task_list:        # 生成任务清单
        template: "驻点任务清单模板"
        data_source: [community_info, history_records]
  
  phase_2_collection:  # 阶段2：现场采集
    - guide_power_room:          # 引导配电房采集
        steps:
          - "请拍摄配电房入口照片"
          - "请描述配电房位置"
          - "请拍摄变压器铭牌"
          - "请记录设备运行状态"
        validation: [photo_required, location_required]
    
    - guide_customer_visit:      # 引导客户走访
        steps:
          - "选择走访客户（从历史清单）"
          - "记录客户反馈"
          - "标记问题类型"
          - "拍照存证（如有）"
    
    - guide_emergency_info:      # 引导应急信息采集
        steps:
          - "拍摄发电车进入点"
          - "拍摄停放点"
          - "拍摄接入点"
          - "记录电缆型号和长度"
  
  phase_3_review:  # 阶段3：智能审核
    - validate_photos:           # 审核照片质量
        tool: image_quality_check
        criteria:
          - clarity: "> 0.7"
          - completeness: "all_required_present"
    
    - validate_data:             # 审核数据完整性
        tool: data_completeness_check
        rules:
          - "必填字段不得为空"
          - "数值范围合理"
          - "日期格式正确"
    
    - generate_summary:          # 生成采集总结
        template: "驻点工作总结模板"

outputs:
  - 任务清单
  - 采集数据（结构化）
  - 审核报告
```

#### Skill 2: 文档自动生成（AutoDocGeneration）

```yaml
skill_id: auto_doc_generation
name: 文档自动生成
description: 基于采集数据自动生成各类业务文档

triggers:
  - command: "/generate-doc {doc_type}"
  - event: "collection_completed"
  - keyword: ["生成报告", "生成简报", "出文档"]

document_types:
  community_power_briefing:      # 小区供电简报
    template: "小区供电简报模板.docx"
    data_sources:
      - table: "小区基础信息"
      - table: "配电房信息"
      - table: "设备台账"
      - table: "客户统计"
    output:
      format: [docx, pdf]
      filename: "{小区名}_供电简报_{日期}.docx"
    sections:
      - 小区基本信息
      - 供电设施概况
      - 客户情况分析
      - 近期工作记录
      - 存在问题及建议

  emergency_power_guide:         # 应急发电指引
    template: "应急发电指引模板.docx"
    data_sources:
      - table: "应急接入信息"
      - table: "配电房信息"
      - table: "物业联系信息"
    output:
      format: [docx, pdf]
      filename: "{小区名}_应急发电指引.docx"
    sections:
      - 小区位置及入口
      - 发电车接入方案
      - 电缆型号及长度
      - 物业联系人
      - 安全注意事项
      - 现场照片

  service_quality_report:        # 优质服务简报
    template: "优质服务简报模板.docx"
    data_sources:
      - table: "客户走访记录"
      - table: "投诉处理记录"
      - table: "满意度调查"
    output:
      format: [docx, pdf]
      filename: "{小区名}_服务简报_{月份}.docx"
    sections:
      - 走访客户情况
      - 问题处理统计
      - 客户满意度
      - 典型案例
      - 下一步工作计划

workflow:
  1_query_data:        # 查询数据
    tool: wps_ksheet_query
    parallel: true
  
  2_fill_template:     # 填充模板
    tool: wps_doc_generate
    params:
      template_id: "{doc_type}"
      data: "{queried_data}"
  
  3_save_to_wps:       # 保存到WPS云
    tool: wps_file_save
    params:
      folder: "/供电所文档/{小区名}/"
      share_with: ["供电所群组"]
  
  4_notify_user:       # 通知用户
    channel: wecom
    message: "文档已生成：{doc_url}"
```

#### Skill 3: 应急处置指引（EmergencyGuide）

```yaml
skill_id: emergency_guide
name: 应急处置指引
description: 在故障和应急情况下指引现场人员完成任务

triggers:
  - command: "/emergency {type}"
  - keyword: ["故障", "停电", "应急", "抢修"]
  - intent: "应急处置"

emergency_types:
  power_outage:        # 停电故障
    priority: high
    workflow:
      - confirm_scope:         # 确认影响范围
          question: "请确认停电影响范围"
          options: ["单户", "整栋楼", "整个小区", "不确定"]
      
      - query_customer_info:   # 查询客户信息
          tool: wps_ksheet_query
          params:
            table: "敏感客户清单"
            filter: "小区 = {community}"
      
      - check_emergency_plan:  # 查阅应急预案
          tool: wps_doc_query
          params:
            doc: "{小区}_应急发电指引"
      
      - guide_response:        # 指导响应
          steps:
            - "立即联系物业确认情况"
            - "安抚敏感客户（清单已提供）"
            - "准备应急发电车（按指引操作）"
            - "拍摄现场照片记录"
            - "每30分钟更新进展"
  
  equipment_failure:   # 设备故障
    priority: high
    workflow:
      - identify_equipment:    # 识别故障设备
          question: "请描述故障现象"
          photo_required: true
      
      - query_device_info:     # 查询设备信息
          tool: wps_ksheet_query
          params:
            table: "设备台账"
            filter: "设备编号 = {device_id}"
      
      - check_safety:          # 安全检查
          checklist:
            - "是否已断电"
            - "是否设置警示标识"
            - "是否通知相关人员"
      
      - guide_repair:          # 指导抢修
          steps:
            - "记录故障现象（拍照）"
            - "联系抢修队伍"
            - "准备备件（参考设备信息）"
            - "监督抢修过程"
            - "验收并记录"

outputs:
  - 应急处理步骤（动态生成）
  - 相关联系人和设备信息
  - 处理记录模板
```

---

## 三、WPS多维表格数据模型

### 3.1 核心表格设计

```yaml
# 1. 小区基础信息表（多维表格）
table_name: 小区基础信息表
columns:
  - 小区ID: string (主键)
  - 小区名称: string
  - 地址: string
  - 物业名称: string
  - 物业联系人: string
  - 物业电话: string
  - 客户总数: number
  - 配电房数量: number
  - 变压器数量: number
  - 敏感客户数: number
  - 上次驻点日期: date
  - 驻点次数: number
  - 创建时间: datetime
  - 更新时间: datetime

# 2. 驻点工作记录表
table_name: 驻点工作记录
columns:
  - 记录ID: string (主键)
  - 小区ID: string (外键)
  - 驻点日期: date
  - 客户经理: string
  - 工作内容: multiline_text
  - 配电房检查: boolean
  - 客户走访数: number
  - 发现问题数: number
  - 解决问题数: number
  - 照片数量: number
  - 状态: enum ["进行中", "已完成", "待审核"]
  - 关联文档: string[] (文档链接)

# 3. 配电房信息表
table_name: 配电房信息
columns:
  - 配电房ID: string (主键)
  - 小区ID: string (外键)
  - 配电房名称: string
  - 位置描述: string
  - 变压器数量: number
  - 变压器容量: string
  - 投运日期: date
  - 设备状态: enum ["正常", "异常", "待检修"]
  - 照片链接: string[]
  - 隐患记录: string

# 4. 应急接入信息表
table_name: 应急接入信息
columns:
  - 小区ID: string (主键)
  - 进入点描述: string
  - 进入点照片: string[]
  - 停放点描述: string
  - 停放点照片: string[]
  - 接入点描述: string
  - 接入点照片: string[]
  - 电缆型号: string
  - 电缆长度: number
  - 接入条件: string
  - 应急联系人: string
  - 应急电话: string

# 5. 客户走访记录表
table_name: 客户走访记录
columns:
  - 记录ID: string (主键)
  - 客户ID: string
  - 小区ID: string (外键)
  - 走访日期: date
  - 走访人: string
  - 客户反馈: multiline_text
  - 问题类型: enum ["停电", "电费", "服务", "其他"]
  - 处理措施: string
  - 满意度: enum ["非常满意", "满意", "一般", "不满意"]
  - 需回访: boolean
```

### 3.2 WPS API调用示例

```javascript
// WPS开放平台API调用示例（Node.js）

const axios = require('axios');

class WPSCloudAPI {
  constructor(app_id, app_secret) {
    this.app_id = app_id;
    this.app_secret = app_secret;
    this.base_url = 'https://open.wps.cn/api';
    this.access_token = null;
  }

  // 获取访问令牌
  async getAccessToken() {
    const response = await axios.post(`${this.base_url}/auth/v1/token`, {
      app_id: this.app_id,
      app_secret: this.app_secret
    });
    this.access_token = response.data.access_token;
    return this.access_token;
  }

  // 查询多维表格数据
  async queryKSheet(table_id, filter = {}) {
    const response = await axios.post(
      `${this.base_url}/ksheet/v1/data/query`,
      {
        table_id: table_id,
        filter: filter,
        limit: 100
      },
      {
        headers: {
          'Authorization': `Bearer ${this.access_token}`
        }
      }
    );
    return response.data.records;
  }

  // 插入记录到多维表格
  async insertRecord(table_id, record) {
    const response = await axios.post(
      `${this.base_url}/ksheet/v1/data/insert`,
      {
        table_id: table_id,
        records: [record]
      },
      {
        headers: {
          'Authorization': `Bearer ${this.access_token}`
        }
      }
    );
    return response.data;
  }

  // 更新记录
  async updateRecord(table_id, record_id, record) {
    const response = await axios.post(
      `${this.base_url}/ksheet/v1/data/update`,
      {
        table_id: table_id,
        record_id: record_id,
        record: record
      },
      {
        headers: {
          'Authorization': `Bearer ${this.access_token}`
        }
      }
    );
    return response.data;
  }

  // 基于模板生成文档
  async generateDocument(template_id, data, output_name) {
    const response = await axios.post(
      `${this.base_url}/doc/v1/generate`,
      {
        template_id: template_id,
        data: data,
        output_name: output_name,
        format: 'docx'
      },
      {
        headers: {
          'Authorization': `Bearer ${this.access_token}`
        }
      }
    );
    return response.data.document_url;
  }
}

// 使用示例
const wps = new WPSCloudAPI('your_app_id', 'your_app_secret');

// 查询小区信息
async function getCommunityInfo(communityName) {
  await wps.getAccessToken();
  
  const records = await wps.queryKSheet('tbl_community', {
    field: '小区名称',
    operator: 'equals',
    value: communityName
  });
  
  return records[0];
}

// 保存驻点记录
async function saveStationRecord(record) {
  await wps.getAccessToken();
  
  const result = await wps.insertRecord('tbl_station_work', {
    小区ID: record.community_id,
    驻点日期: record.date,
    客户经理: record.manager,
    工作内容: record.content,
    状态: '已完成'
  });
  
  return result.record_id;
}

// 生成供电简报
async function generatePowerBriefing(communityId) {
  await wps.getAccessToken();
  
  // 查询相关数据
  const community = await wps.queryKSheet('tbl_community', { id: communityId });
  const powerRooms = await wps.queryKSheet('tbl_power_room', { 小区ID: communityId });
  
  // 生成文档
  const docUrl = await wps.generateDocument(
    'tpl_power_briefing',
    {
      小区名称: community.小区名称,
      客户总数: community.客户总数,
      配电房数量: powerRooms.length,
      // ... 其他数据
    },
    `${community.小区名称}_供电简报_${new Date().toISOString().slice(0,10)}.docx`
  );
  
  return docUrl;
}
```

---

## 四、消息流程设计

### 4.1 典型交互流程：配电房信息采集

```
时间线:
────────────────────────────────────────────────────

[用户]                [Agent]                [WPS云]
  │                      │                      │
  │  "/start-station-work 阳光小区"             │
  │─────────────────────>│                      │
  │                      │                      │
  │                      │  1. 查询小区信息      │
  │                      │─────────────────────>│
  │                      │                      │
  │                      │  2. 查询历史记录      │
  │                      │─────────────────────>│
  │                      │                      │
  │                      │  3. 生成任务清单      │
  │                      │  （含配电房、客户等）  │
  │                      │                      │
  │  "开始配电房信息采集"  │                      │
  │<─────────────────────│                      │
  │  （列出任务清单）     │                      │
  │                      │                      │
  │  "配电房在3号楼地下室" │                      │
  │  [语音]              │                      │
  │─────────────────────>│                      │
  │                      │                      │
  │                      │  4. 语音识别          │
  │                      │  5. 提取位置信息      │
  │                      │  6. 保存到临时数据    │
  │                      │                      │
  │  "已记录：3号楼地下室。请拍摄入口照片"       │
  │<─────────────────────│                      │
  │                      │                      │
  │  [照片]              │                      │
  │─────────────────────>│                      │
  │                      │                      │
  │                      │  7. 照片质量检查      │
  │                      │  8. OCR识别（如有文字）│
  │                      │  9. 保存照片到云存储  │
  │                      │                      │
  │  "照片已保存。请拍摄变压器铭牌"             │
  │<─────────────────────│                      │
  │                      │                      │
  │  [照片]              │                      │
  │─────────────────────>│                      │
  │                      │                      │
  │                      │  10. OCR识别铭牌     │
  │                      │  11. 提取型号/容量   │
  │                      │                      │
  │  "识别到：SCB11-500kVA\n是否正确？"          │
  │<─────────────────────│                      │
  │                      │                      │
  │  "正确"              │                      │
  │─────────────────────>│                      │
  │                      │                      │
  │                      │  12. 保存数据        │
  │                      │─────────────────────>│
  │                      │  （更新配电房信息表）  │
  │                      │                      │
  │  "配电房信息已保存。\n继续采集其他信息？"    │
  │<─────────────────────│                      │
  │                      │                      │

[后续: 继续采集客户走访、应急信息等...]
[最终: 生成驻点工作总结报告]
────────────────────────────────────────────────────
```

---

## 五、关键实现要点

### 5.1 云端部署架构

```yaml
# docker-compose.yaml
version: '3.8'

services:
  openclaw-gateway:
    image: openclaw/gateway:latest
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - WECOM_CORP_ID=${WECOM_CORP_ID}
      - WECOM_AGENT_ID=${WECOM_AGENT_ID}
      - WECOM_SECRET=${WECOM_SECRET}
      - WPS_APP_ID=${WPS_APP_ID}
      - WPS_APP_SECRET=${WPS_APP_SECRET}
      - BAIDU_API_KEY=${BAIDU_API_KEY}
    volumes:
      - ./config:/app/config
      - ./skills:/app/skills
    restart: always

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    restart: always

volumes:
  redis_data:
```

### 5.2 安全措施

```yaml
security:
  # 1. 企业微信消息加密
  message_encryption:
    enabled: true
    algorithm: AES-256-CBC
    
  # 2. WPS API调用安全
  api_security:
    https_only: true
    token_refresh: 3600  # 1小时刷新token
    
  # 3. 数据访问控制
  data_access:
    row_level_security: true  # 行级安全
    user_isolation: true      # 用户数据隔离
    
  # 4. 审计日志
  audit_log:
    enabled: true
    log_level: info
    retention_days: 365
```

---

## 六、下一步行动

1. **确认WPS开放平台权限**
   - 申请WPS开放平台账号
   - 获取AppID和AppSecret
   - 确认多维表格API调用权限

2. **企业微信应用配置**
   - 在企业微信管理后台创建自建应用
   - 配置回调URL和消息加解密
   - 测试消息接收和发送

3. **开发环境搭建**
   - 部署OpenClaw Gateway到云端
   - 配置企业微信Provider
   - 集成WPS API SDK

4. **MVP功能开发**
   - 实现"驻点工作引导"Skill
   - 实现基础数据查询和存储
   - 测试端到端流程

这个设计方案符合你的要求吗？有哪些部分需要调整或深入讨论？