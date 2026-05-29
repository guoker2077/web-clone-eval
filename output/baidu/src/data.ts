export interface SearchResult {
  title: string
  summary: string
  source: string
  url: string
}

const summaryTemplates = [
  '关于「{kw}」的最新资讯与深度解读，涵盖背景介绍、核心要点以及网友热议话题，帮助你快速了解全貌。',
  '{kw} 是近期备受关注的话题。本文从多个角度梳理了相关信息，包括定义、发展历程以及实际应用场景。',
  '想了解 {kw} 吗？这里汇总了权威来源的内容，提供详细说明与实用建议，让你一文读懂。',
  '最新「{kw}」相关报道：业内专家给出分析，结合数据与案例，解析其中的关键问题与未来趋势。',
  '{kw} 全面解析。包含常见问题解答、操作指南以及相关推荐，适合初学者和进阶用户参考阅读。',
  '围绕 {kw} 的讨论持续升温，本页整理了网络上的主流观点与最新动态，内容客观全面。',
  '{kw} 百科：基础概念、相关知识点和延伸阅读一应俱全，是了解该主题的良好起点。',
  '关于 {kw} 的实用攻略，手把手教你从入门到熟练，附带图文说明与注意事项。',
]

const sources = [
  '百度百科',
  '百家号',
  '知乎',
  '人民网',
  '新华网',
  '中国新闻网',
  '百度知道',
  '搜狐',
]

const titleSuffixes = [
  '_百度百科',
  ' - 最新消息汇总',
  '：你需要知道的一切',
  ' 详细解读与分析',
  ' 全面介绍',
  '相关内容推荐',
  ' 最新进展',
  '是什么？一文读懂',
]

export function generateResults(keyword: string, page: number, pageSize = 8): SearchResult[] {
  const kw = keyword.trim() || '百度'
  const results: SearchResult[] = []
  for (let i = 0; i < pageSize; i++) {
    const index = (page - 1) * pageSize + i
    results.push({
      title: `${kw}${titleSuffixes[index % titleSuffixes.length]}`,
      summary: summaryTemplates[index % summaryTemplates.length].replace(/\{kw\}/g, kw),
      source: sources[index % sources.length],
      url: `https://www.baidu.com/s?wd=${encodeURIComponent(kw)}&pn=${index}`,
    })
  }
  return results
}

export const navLinks = ['新闻', 'hao123', '地图', '贴吧', '视频', '图片', '网盘', '学术', '更多DuMate', '设置']

export const hotList = [
  '中央气象台发布暴雨黄色预警',
  '专家称应警惕“假理财”',
  '14岁少年勇救落水者 获表彰',
  '多地迎来降温 注意添衣保暖',
  '“低空经济” 释放新动能',
  '新能源汽车销量再创新高',
  '人工智能助力医疗诊断 提升效率',
  '高校毕业生超200万 就业季来临',
  '消费市场持续回暖 信心增强',
  '城市更新行动加速推进',
]
