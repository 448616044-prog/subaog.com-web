# subaog.com SEO Sprint 全面分析 — 2026-08-23

> 基于最新 GSC 拉取（28 天窗口）+ 站点结构实测 + SEO-FRAMEWORK.md
> 分析师：SeoExpert | 数据时点：2026-08-23 23:xx（GMT+8）

---

## 一、数据快照（最新真实状况）

| 指标 | 数值 | 解读 |
|:---|:---|:---|
| Sitemap 提交 | **1833** URL | 内容矩阵已铺满（zh-cn 917 + en 917） |
| Sitemap 收录（GSC 报告） | **0** | ⚠️ GSC 报告延迟（warnings=0/errors=0/pending=False，已接受） |
| 实际有搜索数据的页面 | **91** 页 | 真实已收录≈91+ 页，但**收录率 <5%** |
| 有数据关键词 | **21** 个 | 词库极早期 |
| 28 天总展现 | **190**（页面维度）/ 46（词维度） | 曝光量极低 |
| 28 天总点击 | **2** | 转化尚未起步 |
| 排名分段（21 词） | top3=1 / top10=1 / **11-30=4** / 31-100=15 | 多数词在 3 页外 |
| 设备 | Mobile 55 展现 / Desktop 61 / Tablet 2 | 移动为主，需 Mobile-First 友好 |
| 国家 | usa 45 / can 5 / deu 10 / 其余零散 | 美国是主战场（符合定位） |

**📌 一句话结论**：站点处于**新域首月索引爬坡期**。瓶颈**不是内容量**（1833 页已就绪），而是 **①抓取/收录速度 ②域名权威度(DR=0) ③URL 规范化收敛**。此刻盲目加新页面边际收益极低——应先打通抓取、聚合信号、把已排名词推上首页。

---

## 二、各维度分析与 Sprint 可行动方案

### A. 技术 SEO（🔴 最高优先级 — 打通抓取与规范）

| 问题 | 证据 | 影响 | Sprint 动作 | 工时 |
|:---|:---|:---|:---|:---|
| **URL 规范化碎片化** | GSC 同内容多形态：`/en/blog/x.html`(28展现) + `/en/blog/x`(8) ；`/city/miami-to-shanghai`(排名4) + `/zh-cn/city/miami-to-shanghai`(排名10.7) | 权重分散、收录慢、重复内容风险 | ①全站审计 extensionless vs .html 双形态 ②确认 Cloudflare 仅服务 canonical 形态 ③`_redirects` 已 301 根路径→/zh-cn/，需补 blog extensionless→.html 301 | 中 |
| **Sitemap 收录=0（抓取慢）** | 1833 提交仅 91 页有数据 | 1600+ 页未进入索引池 | ①GSC 提交 6 个新对比页 + 重点 pillar 加速收录 ②提交 URL Inspection API 批量促进 ③检查 robots.txt 无误封 | 低 |
| **孤儿页风险** | 800 城市组合页 + 25 can-i-ship 需确认有入链 | 无入链页不被抓取 | 用脚本审计 body 内链，给真孤儿补"相关推荐"框 | 低 |
| **Core Web Vitals** | 框架要求 LCP<2.5s/INP<200ms | 移动排名因子 | 用 PageSpeed 实测首页+pillar，图片 WebP 化 | 中 |

**Sprint A 交付**：规范化审计报告 + 补 `_redirects` 规则 + 孤儿页补链 + GSC 加速提交。

---

### B. 短词（short-tail）— 🟡 准备期，不硬冲

短词 = `ship to china` / `shipping to china` / `usa to china shipping` / `美国寄中国`。
当前数据：`shipping to china` 排名 30.8（4 展现）、`shipping usa to china` 排名 95。

| 判断 | 说明 |
|:---|:---|
| 竞争度 | 高（国际快递官网 + 大媒体），DR=0 新域无法正面争 |
| 当前策略 | **先建好 Pillar 承接页**，等 DR 起来（你明天的任务）再冲 |
| 已具备 | `/usa-to-china/`（Pillar）、`/en/usa-to-china/` 已存在 |
| Sprint 可做的**准备** | ①强化 Pillar 内容深度（费用表/时效表/案例）②确保 Pillar 拿到全站最强内链 ③预留 FAQPage/Table Schema |

**不建议**本 Sprint 程序化生成短词页面——收录不了也排不上去，浪费抓取预算。

---

### C. 中词（mid-tail）— 🟢 最高转化杠杆，立即推

中词 = 带修饰的具体词，当前已现 4 个排 11-30（**冲首页窗口**）：

| 关键词 | 排名 | 对应页 | Sprint 动作 |
|:---|:---|:---|:---|
| `dhl to china` | 18.0 | /en/blog/dhl-vs-fedex-vs-ups-china | 加 3+ 上下文内链 + 内容补 DHL 专节 |
| `san diego to hangzhou` | 14.0 | /en/city/san-diego-to-hangzhou | 城市页互链强化 + Schema LocalBusiness |
| `miami to shanghai` | 10.7 | /zh-cn/city/miami-to-shanghai | 中文城市页内链矩阵 |
| `seasia singapore` | 10.3 | /zh-cn/seasia-to-china/singapore/ | 东南亚线 pillar 内链 |

**通用打法**（从 subao.tw 验证有效）：对这 4 页——①从 6 个 hub 页注入上下文内链 ②补 FAQPage 长尾问 ③GSC 单独提交加速 ④内容加深 200-300 字。预计 2-4 周可进首页，带来首批稳定点击。

---

### D. 工具页（tools）— 🟢 已建成，现在是"链接磁铁"打磨

框架列 5 个工具，**实测全部就位且 Schema 完整**：

| 工具 | 文件 | Schema | 状态 |
|:---|:---|:---|:---|
| 运费计算器 | shipping-calculator.html | WebApplication ✅ | 可用 |
| 关税估算器 | customs-duty-calculator.html | WebApplication ✅ | 可用 |
| 材积计算器 | volume-calculator.html | WebApplication ✅ | 可用 |
| 时效查询 | transit-time.html | FAQPage ✅ | 可用 |
| 能不能寄 | can-i-ship.html | FAQPage ✅ | 可用 |

**Sprint 动作**：
1. 确认 5 工具页**全部入 sitemap + 有 header/footer 入链**（链接磁铁需被爬到）
2. 给工具页加"相关 Blog 推荐"侧链（框架 7.2 要求，提升工具页权重传导）
3. 提交 GSC 加速收录——工具页是**自然外链最容易获得的资产**（用户明天 DR 建设时优先推工具页）
4. 计算器页加 `WebApplication` + `potentialAction` 富结果标记，争富摘要

---

### E. 流量聚合页（traffic aggregation）— 🟢 填补空白，提升抓取+主题权威

现有聚合页：blog/index（60 卡）、usa-to-china pillar、各线路 index（japan/seasia/korea/australia/canada/europe-to-china）。

**缺口**（本 Sprint 高价值新建）：
1. **「美国寄中国」超级枢纽页**：聚合 800 城市组合页 + 25 can-i-ship + 6 对比页 + 工具页，一个导航型 hub 提升抓取覆盖率与主题权威。
2. **can-i-ship 分类枢纽**：当前 25 品类挤在一个长页，拆成 5-6 个分类 hub（保健品/化妆品/电子/家居/食品/特殊品），每个链回具体品类页。
3. **线路总览页** `/routes/`：把 7 条线路（usa/japan/korea/seasia/australia/canada/europe → china）做成索引，互链成网。

**价值**：聚合页是"内链枢纽"，直接解决 1600+ 页抓取不到的问题（Sprint A 的孤儿页补链可借聚合页一次性完成）。

---

## 三、Sprint 优先级总表

| 优先级 | 动作 | 类型 | 工时 | 预期收益 | 依赖 |
|:---|:---|:---|:---|:---|:---|
| **P0** | URL 规范化修复（补 _redirects + 审计双形态） | 技术 | 中 | 消除权重分散，加速收录 | 无 |
| **P0** | GSC 加速提交（6 对比页 + 重点 pillar + 5 工具页） | 技术 | 低 | 缩短收录周期 | 无 |
| **P1** | 中词 4 页推首页（内链+内容+提交） | 中词 | 低 | 首批稳定点击 | 无 |
| **P1** | 流量聚合页（超级枢纽 + can-i-ship 分类 + 线路总览） | 聚合 | 中 | 解决孤儿页+主题权威 | P0 |
| **P1** | 工具页链接磁铁打磨（侧链+富结果+提交） | 工具 | 低 | 承接明天 DR 外链 | 无 |
| **P2** | Pillar 内容加深（承接短词，等 DR 冲） | 短词 | 中 | 为 DR 后冲短词铺路 | 明天 DR |
| **P2** | CWV 实测+图片 WebP 化 | 技术 | 中 | 移动排名因子 | 无 |

---

## 四、建议本次执行清单（确认后我全量执行）

1. ✅ **规范化修复脚本**：扫描全站 extensionless/.html 双形态 + 根路径泄漏，输出报告并补 `_redirects`。
2. ✅ **孤儿页审计+补链**：脚本审计 800 城市组合页 + 25 can-i-ship 入链，真孤儿补"相关推荐"框。
3. ✅ **中词 4 页优化**：gen 脚本注入内链 + FAQ 补长尾问 + GSC 提交。
4. ✅ **3 个聚合页生成器**：超级枢纽 / can-i-ship 分类 / 线路总览（中英双语）。
5. ✅ **GSC 批量提交**：6 对比页 + 5 工具页 + 3 pillar 经 URL Inspection API 促收录。
6. ✅ 上述全部 commit + push 部署。

> 短词硬冲与 CWV 深度优化列为 P2，建议 DR 建设（你明天任务）启动后再做，避免抓取预算浪费。

---

*分析基于：GSC API 拉取（代理 127.0.0.1:17891 + JWT）、站点结构实测、SEO-FRAMEWORK.md v1.0*
