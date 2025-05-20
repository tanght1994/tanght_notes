# 提示套路

- 等效/等价法：用等效/等价的写法将上面的代码修改为简单易懂的格式，然后教会我理解上面的代码
- 对比法：对于这个参数，传递不同的参数来对比一下效果，通过对比的方法来向我解释上面的代码

- X 的作用是什么？写一个demo，对比使用 X 和不使用 X 在代码上的区别，进而说明 X 的作用



```base
你是一名专业的教师，擅长设计教学大纲，你擅长将复杂的知识拆分成简单易懂的小知识点，帮助学生更好地理解和掌握知识。
相关联的知识点要放在同一个章节，且知识点要由浅入深，循序渐进。
你的输出格式为json，格式如下：
{
  "book": [
    {
      "chapter_name": "此章节的名字",
      "knowledges": [本章节需要包含的知识点、api、class、函数、概念等等，只需列举出来，不需要解释]
    },
    ...
  ]
}
请你设计一个从基础的css逐步过渡到Tailwind CSS的学习大纲。


你是一名专业的教师，请按照教学大纲，完成"CSS 预处理器基础"这个章节的编写，要尽量使用简单易懂的demo来演示。
同时解释为什么需要CSS 预处理器，什么是预处理器，预处理器的好处是什么？如果没有预处理器，CSS会有什么问题？
完成"Tailwind CSS 入门"这个章节的编写，一定要尽量详细，因为我没有任何基础。多用简单易懂的demo来演示。
教学大纲开始
{
  "book": [
    {
      "chapter_name": "CSS 基础入门",
      "knowledges": [
        "CSS 语法与选择器",
        "盒模型（margin, padding, border）",
        "常用单位（px, em, rem, %）",
        "文本样式（font-size, color, line-height）",
        "基础布局（display, position）",
        "浮动与清除浮动",
        "Flexbox 基础"
      ]
    },
    {
      "chapter_name": "响应式设计与布局进阶",
      "knowledges": [
        "媒体查询（media queries）",
        "视口单位（vw, vh）",
        "Grid 布局基础",
        "Flexbox 进阶",
        "响应式图片处理",
        "移动优先原则"
      ]
    },
    {
      "chapter_name": "CSS 预处理器基础",
      "knowledges": [
        "变量（variables）",
        "嵌套语法",
        "Mixin 与函数",
        "模块化组织",
        "编译流程"
      ]
    },
    {
      "chapter_name": "Tailwind CSS 入门",
      "knowledges": [
        "实用类（Utility Classes）概念",
        "安装与配置（PostCSS 集成）",
        "核心配置文件（tailwind.config.js）",
        "响应式断点（sm, md, lg）",
        "状态变体（hover, focus）",
        "颜色系统与间距系统"
      ]
    },
    {
      "chapter_name": "Tailwind 样式系统",
      "knowledges": [
        "排版系统（font-size, line-height）",
        "盒模型工具（margin, padding）",
        "Flexbox 与 Grid 工具类",
        "定位与层叠上下文",
        "背景与渐变",
        "过渡与动画"
      ]
    },
    {
      "chapter_name": "Tailwind 高级特性",
      "knowledges": [
        "自定义主题配置",
        "插件开发",
        "@apply 指令",
        "Dark Mode 实现",
        "JIT 模式原理",
        "PurgeCSS 优化"
      ]
    },
    {
      "chapter_name": "项目实战与最佳实践",
      "knowledges": [
        "设计系统构建",
        "组件化开发模式",
        "响应式开发流程",
        "性能优化策略",
        "与框架集成（React/Vue）",
        "调试技巧与常见问题"
      ]
    }
  ]
}
教学大纲结束

```









# 术语、概念

## 关键词扩展

使用LLM从问题中提取关键词（如实体、术语），追加到原始问题后，增强检索的召回率。
示例：问题“如何解决连接超时？”可能扩展为“如何解决连接超时？关键词：网络故障、服务器配置、防火墙设置”。

## 多轮对话重写

利用LLM将多轮对话历史合并为更完整的单问题，提升检索准确性。

## MCP

一种为大模型提供环境信息的协议，让人类实现function call更加简单方便。

mcp inspector

## agents.json

一种为大模型提供环境信息的协议，让人类实现function call更加简单方便。

## 推理（reasoning）

## NLP

分词：将一段话分为一个个独立的词语

词性：动词、名词、形容词等，不同的词性重要程度不一样

## 嵌入（embedding）

任何一句人类语言都可以转变为一个固定维度的向量（比如1024维度），不管输入的长度是多少，输出长度永远是固定的（比如1024维度）。

需要使用大模型对文本进行嵌入，各大公司都提供了embeding模型。

vec = embedding("一些文本，可长可短，随意")。

不管输入的字符串长度为多少，vec长度都是固定的，比如1024。

vec = [0.00123, 0.21321, 0.1111, ...]

## Function Call

ChatGPT指定的格式，用于LLM调用程序员提供的外部工具。

程序员需要详细的描述各个Tool的功能和参数，然后将这些描述放在LLM的提示词中（tool字段中），这样LLM就能够在适当的时候调用适当的tool了。

如何详细的描述Tool的功能和参数？类似API文档就行了，总之描述越清晰，LLM就能约准确的使用工具。

MCP 和 OpenAPI 是目前两种有前途的方式。

## OpenAPI

最受程序员认可的 API 文档格式，由 swagger 公司维护，后来改名为 OpenAPI 了。

使用 OpenAPI 的格式向 LLM 提供 api 描述，效果非常好。

## swagger

规范API文档

- 在代码的注释中，按照 swagger 的格式编写文档，例如参数是什么，各参数的作用是什么，此API的作用是什么
- 然后 swagger 就能从注释中提取相关信息，生成 swagger.yaml 文件
- 然后 swagger 根据 swagger.yaml 生成一个HTTP网页，便于人类查看API文档

## swagger editor

手动编写 swagger.yaml 实时预览API文档效果

网址 https://editor.swagger.io/

## OpenAI

一家公司，发明了**ChatGPT**，开启了全民聊天形AI时代

## Anthropic

OpenAI 离职员工创办的公司，产品是**Claude**， 对标ChatGPT