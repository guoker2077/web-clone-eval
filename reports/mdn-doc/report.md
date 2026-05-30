# 一致性评估报告：MDN <a> 元素文档页

- 原始网址：https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a
- 复刻类型：content
- **综合得分：80.2 / 100**

> 度量可置信性说明：标注 `确定性` 的指标（SSIM/像素差/pHash/各覆盖率）为精确计算，同一输入必得同一结果、可复现；标注 `非确定` 的 LLM 视觉分为辅助信号，不计入主总分，仅用于与确定性指标交叉验证（见下文）。所有比率均附原始计数（分子/分母），便于核对。

## 维度得分

| 维度 | 得分 | 权重 | 性质 |  |
| --- | --- | --- | --- | --- |
| 视觉一致性 | 50.6 | 0.4 | 确定性·可复现 | `██████████░░░░░░░░░░` |
| 功能一致性 | 100.0 | 0.4 | 确定性·可复现 | `████████████████████` |
| 交互一致性 | 100.0 | 0.2 | 确定性·可复现 | `████████████████████` |

## 视觉指标明细（确定性·可复现）

### 范围对齐：逐声明模块裁剪比对（主分依据）

> 只比对 scope 声明的模块区域（原页 box 来自 capture，复刻页来自 data-testid），避免整页比对被范围外内容拉低。

| 视口 | 模块 | SSIM↑ | 像素差异率↓ | pHash距离↓ | 状态 |
| --- | --- | --- | --- | --- | --- |
| desktop | skip-to-content | — | — | — | ❌ 缺失/不可比 |
| desktop | logo-home | 0.3751 | 0.293 | 30 | ✓ |
| desktop | nav-blog | 0.6277 | 0.1415 | 12 | ✓ |
| desktop | breadcrumb-web | — | — | — | ❌ 缺失/不可比 |
| desktop | breadcrumb-html | — | — | — | ❌ 缺失/不可比 |
| desktop | breadcrumb-reference | — | — | — | ❌ 缺失/不可比 |
| desktop | breadcrumb-elements | — | — | — | ❌ 缺失/不可比 |
| desktop | breadcrumb-anchor | 0.8802 | 0.1329 | 16 | ✓ |
| desktop | toc-try-it | 0.3592 | 0.1472 | 42 | ✓ |
| desktop | toc-attributes | 0.4261 | 0.1762 | 32 | ✓ |
| desktop | toc-accessibility | 0.4194 | 0.1837 | 28 | ✓ |
| desktop | toc-examples | 0.4188 | 0.1731 | 32 | ✓ |
| desktop | toc-security-privacy | 0.4249 | 0.1837 | 22 | ✓ |
| desktop | toc-technical-summary | 0.4675 | 0.1746 | 28 | ✓ |
| desktop | toc-specifications | 0.4277 | 0.1799 | 26 | ✓ |
| desktop | toc-browser-compatibility | 0.4301 | 0.1231 | 34 | ✓ |
| desktop | toc-see-also | 0.4447 | 0.157 | 38 | ✓ |
| desktop | content-global-attributes | — | — | — | ❌ 缺失/不可比 |
| desktop | content-attr-download | 0.5297 | 0.3088 | 12 | ✓ |
| desktop | content-attr-hreflang | 0.5436 | 0.2966 | 8 | ✓ |
| desktop | **聚合(14/20)** | **0.4839** | **0.1908** | **25.7** | — |

### 整页比对（参考，不作主分）

> 含范围外内容，仅留档对照；对部分复刻天然偏低，不代表复刻质量。

| 视口 | SSIM↑ | 像素差异率↓ | pHash距离↓ |
| --- | --- | --- | --- |
| desktop | 0.5801 | 0.1212 | 20 |

## 交叉验证（可置信度）

> 用两种**独立**方法测同一对象，相互印证：确定性指标（SSIM 等，可复现）与 LLM 视觉分（非确定，独立视角）。二者接近则结论可信。

- 确定性视觉分：**50.6**
- LLM 视觉分（均值）：**84.0**
- 差距：**33.4**（阈值 15.0）
- 判定：⚠️ 存疑——两法差距偏大，建议人工复核视觉评分

## LLM 辅助视觉评分（交叉验证，不计入主总分）

> 让 Claude 视觉模型同时看原页与复刻页，按 rubric 打分。评分已对齐复刻范围：只评 scope 声明的模块，范围外内容缺失不扣分。因 LLM 评分非确定性，仅作辅助信号与上方确定性指标交叉验证。

| 视口 | 布局 | 配色 | 排版 | 组件 | 总评 | 点评 |
| --- | --- | --- | --- | --- | --- | --- |
| desktop | 84 | 86 | 85 | 82 | **84** | 指定模块整体还原到位，导航、面包屑、右侧大纲与属性锚点结构清晰，仅顶部 Skip 链接缺失、主导航项与原页略有出入。 |

### 逐模块还原度（复刻范围内）

| 视口 | 模块 | 得分 | 说明 |
| --- | --- | --- | --- |
| desktop | 顶部「Skip to main content」跳转链接 | **30** | 复刻页未见该跳转链接，原页左上角有 |
| desktop | 顶部导航栏 MDN 站点 logo | **95** | mdn_ logo 位置与样式还原准确 |
| desktop | 顶部导航栏「HTML」分类菜单按钮 | **80** | 存在且带下拉标识，但主导航整体菜单项与原页排列不同 |
| desktop | 顶部导航栏「Learn」分类菜单按钮 | **82** | 保留 Learn 下拉按钮，位置略有差异 |
| desktop | 顶部导航栏「Blog」链接 | **88** | Blog 链接位置与样式基本一致 |
| desktop | 面包屑导航「Web」链接 | **92** | 蓝色链接样式与位置还原好 |
| desktop | 面包屑导航「HTML」链接 | **92** | 分隔与对齐准确 |
| desktop | 面包屑导航「Reference」链接 | **92** | 层级清晰还原 |
| desktop | 面包屑导航「Elements」链接 | **92** | 样式一致 |
| desktop | 面包屑导航当前页「<a>」链接 | **90** | 当前页项还原，分隔符用斜杠略不同 |
| desktop | 右侧 On this page 大纲「Try it」锚点 | **90** | In this article 列表首项一致 |
| desktop | 右侧大纲「Attributes」锚点 | **90** | 顺序与文字还原准确 |
| desktop | 右侧大纲「Accessibility」锚点 | **90** | 位置与样式一致 |
| desktop | 右侧大纲「Examples」锚点 | **90** | 还原到位 |
| desktop | 右侧大纲「Security and privacy」锚点 | **90** | 文字与层级一致 |
| desktop | 右侧大纲「Technical summary」锚点 | **90** | 还原准确 |
| desktop | 右侧大纲「Specifications」锚点 | **90** | 顺序正确 |
| desktop | 右侧大纲「Browser compatibility」锚点 | **90** | 文字一致 |
| desktop | 右侧大纲「See also」锚点 | **90** | 末项还原准确 |
| desktop | 正文中「global attributes」链接 | **88** | 蓝色链接位置与上下文一致 |
| desktop | Attributes 章节内「download」属性锚点链接 | **85** | 蓝色徽章样式锚点还原，但章节顺序与原页排列略有不同 |
| desktop | Attributes 章节内「hreflang」属性锚点链接 | **85** | 锚点徽章样式一致，位置接近 |

## 功能覆盖（确定性·可复现）

- 元素存在率：22/22（100.0%）
- 行为通过率：4/4（100.0%） 个功能点全通过
- 断言通过率：9/9（100.0%） 条断言

### 交互断言明细

- ✅ **header-visible** (2/2)
  - ✓ `expect_visible(logo-home)`
  - ✓ `expect_visible(nav-blog)`
- ✅ **breadcrumb-check** (2/2)
  - ✓ `expect_visible(breadcrumb-web)`
  - ✓ `expect_text(breadcrumb-anchor='<a>')`
- ✅ **toc-jump-attributes** (3/3)
  - ✓ `click(toc-attributes)`
  - ✓ `expect_visible(content-attr-download)`
  - ✓ `expect_visible(content-attr-hreflang)`
- ✅ **toc-content-check** (2/2)
  - ✓ `expect_text(toc-specifications='Specifications')`
  - ✓ `expect_text(toc-see-also='See also')`

## 评估结论

复刻基本可用，主要功能实现，视觉或交互存在可改进项。

> 指标说明：SSIM 为结构相似度(0-1，越高越好)；像素差异率为超阈值像素占比；
> pHash 距离为感知哈希汉明距离(0-64，越低越相似)。所有截图统一缩放后比较，
> 动态区域已按 scope.masks 遮罩。
