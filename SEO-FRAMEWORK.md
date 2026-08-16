# subaog.com SEO 完整框架 — Phase 1: 美国→中国

> 基于 subao.tw 成功模式提炼 + 项目2 SPEC 改编
> 搜索引擎：Google 为主（用户用中文搜索美国寄中国相关问题）

---

## 一、品牌与定位

| 项目 | 内容 |
|:---|:---|
| 品牌名 | 速豹国际物流 (Subao Global) |
| 域名 | subaog.com |
| Phase 1 定位 | 美国寄中国物流专家 |
| Slogan | 美国到中国，速豹更快更省 |
| 目标用户 | 美国华人/留学生/代购/企业 |
| 语言策略 | 简体中文为主 (zh-CN)，部分内容双语 |
| 核心优势 | 华人渠道、价格透明、时效稳定、全程追踪 |

---

## 二、用户画像与搜索意图

| 用户群 | 典型搜索词 | 意图类型 | 内容策略 |
|:---|:---|:---|:---|
| 留学生 | 美国寄行李回国多少钱 / 留学生回国邮寄 | Transactional | 场景页 + 计算器 |
| 华人代购 | 美国保健品寄回国 / 美国寄化妆品到中国 | Transactional | 品类长尾集群 |
| 搬家族 | 从美国搬家回中国 / 美国家具海运回国 | Transactional | 服务详情页 |
| 企业客户 | 美国到中国海运专线 / 商业样品寄中国 | Commercial | 案例 + 资质展示 |
| 比价用户 | 美国寄中国哪家快递便宜 / USPS vs 华人快递 | Commercial | 对比评测页 |
| 信息查询 | 美国寄中国要交税吗 / 禁运物品清单 | Informational | Blog + FAQ |

---

## 三、话题集群架构 (Topic Clusters)

### Pillar 1: 美国寄中国全攻略 (route: /usa-to-china)
```
/usa-to-china/                          ← Pillar Page（美国寄中国终极指南）
├── /blog/usps-vs-fedex-vs-chinese-courier    ← 对比评测 Cluster
├── /blog/usa-to-china-sea-freight            ← 海运专线
├── /blog/usa-to-china-air-freight            ← 空运专线
├── /blog/usa-to-china-customs-duty           ← 关税指南
└── /blog/usa-to-china-prohibited-items        ← 禁运清单
```

### Pillar 2: 留学生回国行李 (route: /student-luggage)
```
/student-luggage/                       ← Pillar Page
├── /blog/student-luggage-cost-calculator     ← 费用详解
├── /blog/student-luggage-packing-guide       ← 打包攻略
├── /blog/student-luggage-customs             ← 清关避坑
└── /blog/student-luggage-vs-excess-baggage   ← vs 超重行李对比
```

### Pillar 3: 美国搬家回中国 (route: /usa-moving-to-china)
```
/usa-moving-to-china/                   ← Pillar Page
├── /blog/moving-furniture-usa-to-china       ← 家具海运
├── /blog/moving-cost-breakdown               ← 费用明细
├── /blog/moving-timeline                     ← 搬家时间线
└── /blog/moving-insurance                    ← 运输保险
```

### Pillar 4: 品类长尾集群（核心流量金矿）
```
/blog/can-i-ship-supplements-to-china         ← 保健品
/blog/can-i-ship-cosmetics-to-china           ← 化妆品
/blog/can-i-ship-electronics-to-china         ← 电子产品
/blog/can-i-ship-luxury-bags-to-china         ← 奢侈品
/blog/can-i-ship-baby-formula-to-china        ← 奶粉
/blog/can-i-ship-wine-to-china                ← 红酒
/blog/can-i-ship-books-to-china               ← 书籍
/blog/can-i-ship-shoes-to-china               ← 鞋子衣服
/blog/can-i-ship-medical-devices-to-china     ← 医疗器械
/blog/can-i-ship-coffee-to-china              ← 咖啡
... (扩展至 50+ 品类)
```

### Pillar 5: 城市出发/到达交叉页
```
/city/ny-to-beijing                          ← 纽约→北京
/city/la-to-shanghai                         ← 洛杉矶→上海
/city/sf-to-guangzhou                        ← 旧金山→广州
/city/chicago-to-shenzhen                    ← 芝加哥→深圳
/city/houston-to-chengdu                     ← 休斯顿→成都
/city/seattle-to-beijing                     ← 西雅图→北京
... (扩展至美国TOP20城市 × 中国TOP15城市)
```

---

## 四、工具页矩阵（链接资产 + 流量引擎）

| 工具 | URL | Schema | 功能 |
|:---|:---|:---|:---|
| 国际运费计算器 | /tools/shipping-calculator | WebApplication | 输入重量+路线→预估运费 |
| 关税估算器 | /tools/customs-duty-calculator | WebApplication | 品类+价值→预估关税 |
| 材积计算器 | /tools/volume-calculator | HowTo + WebApp | 长×宽×高÷5000 |
| 能不能寄查询 | /tools/can-i-ship | FAQPage | 品类→是否可寄+替代方案 |
| 时效查询 | /tools/transit-time | WebApplication | 路线→预估时效 |

---

## 五、页面架构 (完整URL结构)

```
/
├── index.html                         ← 首页（美国→中国双渠道入口）
├── usa-to-china/                      ← Pillar 1（美国寄中国全攻略）
│   ├── index.html
│   ├── air-freight.html
│   ├── sea-freight.html
│   └── express.html
├── student-luggage/                   ← Pillar 2（留学生行李）
│   └── index.html
├── usa-moving-to-china/               ← Pillar 3（搬家回国）
│   └── index.html
├── pricing.html                       ← 价格页（阶梯报价表）
├── blog/                              ← Blog 文章（50+ 篇）
├── tools/                             ← 五大工具页
├── city/                              ← 城市交叉页（20×15 = 300页）
├── about.html                         ← 关于我们
├── contact.html                       ← 联系我们
├── faq.html                           ← 常见问题
└── track.html                         ← 物流追踪
```

---

## 六、技术SEO规范（复用自 subao.tw 经验）

### 6.1 每页必加载
- `<meta name="viewport">` + `applicable-device: pc,mobile`
- Canonical URL（self-referencing）
- BreadcrumbList Schema
- FAQPage/Article/HowTo/WebApplication Schema（按页面类型）
- Organization Schema（含 logo + contactPoint）
- OG 标签（og:title/description/image/type/url）
- 百度/Google 验证代码（Phase 1 不做百度，但预留）
- GA4 跟踪代码
- indexnow key（Bing/ChatGPT 流量）
- **禁止 noindex**（防回退规则）

### 6.2 性能基线
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1
- 图片：WebP 格式，<100KB
- CSS 内嵌于 `<style>`（减少 HTTP 请求）
- 无外部字体加载（系统字体优先）
- CDN 加速（Cloudflare 或类似）

### 6.3 结构化数据
每页根据内容类型加载对应 Schema：
- 首页：Organization + FAQPage + BreadcrumbList
- Blog：Article + FAQPage + BreadcrumbList
- 工具页：WebApplication + HowTo + BreadcrumbList
- 价格页：Table + BreadcrumbList
- 城市页：LocalBusiness + BreadcrumbList

### 6.4 robots.txt
```
User-agent: *
Allow: /
Sitemap: https://subaog.com/sitemap.xml

User-agent: Baiduspider
Allow: /
Crawl-delay: 1
```

---

## 七、内链策略（核心——从 subao.tw 验证有效）

### 7.1 集群内链规则
- Pillar → Sub-pages: 每个 Pillar 页面链接所有 cluster 子页面
- Sub-pages → Pillar: 所有 cluster 子页面必须链接回 Pillar
- Cross-cluster: 相关主题间相互引用（如海运文章链接搬家文章）

### 7.2 侧链注入规则
- 每个 Blog 文章至少 3 条上下文内链到相关页面
- 工具页嵌入相关 Blog 文章推荐
- 城市页链接到对应路线页

### 7.3 全局导航
- Header: 核心服务 | 价格 | 工具 | Blog | 追踪 | 联系
- Footer: 完整站点地图 + 联系方式

---

## 八、内容日历 — 首批250篇

### 第一批（核心20篇）：Pillar + 高转化工具
1. 美国寄中国终极指南 2026（Pillar 1）
2. 留学生回国行李邮寄全攻略（Pillar 2）
3. 美国搬家回中国完整指南（Pillar 3）
4. 五大工具页 × 5
5. 国际运费对比：USPS vs FedEx vs UPS vs 华人快递
6. 美国寄中国关税终极指南
7. 美国寄中国禁运物品清单
8. 美国保健品寄中国攻略
9. 美国化妆品寄中国攻略
10. 美国电子产品寄中国指南
11. 美国寄中国多少钱（各渠道价格对比）
12. 美国海运回国 vs 空运回国怎么选
13. 美国寄中国时效全对比
14. 美国寄中国最便宜的方式
15. 美国寄中国打包技巧大全
16. 美国寄中国报关流程详解

### 第二批（50篇）：品类长尾集群
美国寄XX到中国 — 覆盖 50 个品类

### 第三批（180篇）：城市交叉页
美国TOP20城市 → 中国TOP15城市（部分通过程序化生成）

---

## 九、三阶段扩展路线

| 阶段 | 时间 | 线路 | 新增内容 | 目标 |
|:---|:---|:---|:---|:---|
| Phase 1 | 当前 | 美国→中国 | 250+ 页面 | 上线即覆盖核心流量 |
| Phase 2 | Q4 2026 | + 中国→中东 | 新增150+页面 | 覆盖中东线需求 |
| Phase 3 | 2027 | + 俄罗斯/北美/欧洲 | 新增200+页面 | 全球线路矩阵 |

---

## 十、关键KPI（Phase 1 上线后三个月）

| 指标 | 目标 |
|:---|:---|
| 页面总数 | 250+ |
| Google 收录率 | 80%+ |
| 月均自然流量 | 10,000+ |
| 核心词排名 | 美国寄中国 前3页 |
| 长尾词覆盖 | TOP50 词中占 30% |
| 工具页入链数 | 5+ 自然外链 |
| Core Web Vitals | 全部 PASS |

---

*框架版本：v1.0 | 更新日期：2026-08-07 | 基于 subao.tw 6个月实战经验*
