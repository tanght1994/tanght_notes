# 提示套路

- 等效/等价法：用等效/等价的写法将上面的代码修改为简单易懂的格式，然后教会我理解上面的代码
- 对比法：对于这个参数，传递不同的参数来对比一下效果，通过对比的方法来向我解释上面的代码

- X 的作用是什么？写一个demo，对比使用 X 和不使用 X 在代码上的区别，进而说明 X 的作用

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

# 产品

FLUX：使用自然语言进行修图

https://playground.bfl.ai/image/generate

https://dashboard.bfl.ai/

即梦：使用自然语言进行修图



react native：使用react创建APP

expo：