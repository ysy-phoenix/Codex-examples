# Codia 代码修复模块

## 简介

随着当前大语言模型的发展，可以将 APR(Automated Program Repair) 也视为一项序列生成任务，并利用 LLMC(Large Language Model Trained on Code) 来解决它。

所利用的主要是 OpenAI 的 Codex 以及 GPT 系列。

> 遗憾的是，在 2023 年 3 月，OpenAI 官方宣布 Codex 相关 API 已经 deprecated。目前用的 model 主要为 `text-davinci-003`

与寻常的程序修复不同，针对 OJ 提交的程序，有如下特点：

- 具有题目的文本描述；
- 待修复的程序通常为函数级；
- 具有充足的测试样例；
- 有 OJ 平台提供的编译、运行时的警告或报错信息作为参考；
- 有标准程序或不同学生编写的正确程序作为参考；
- 有通一学生的历史提交作为参考；

其中后几点与少样本学习的过程较为契合，通过提供的多重信息，帮助生成 prompt，以使得大模型更好地发挥作用。

整个代码修复模块框架的概念图如下：

![](.\assets\framework.png)

主体分为语法修复和语义修复两阶段。

* **语法修复阶段：**
  * 首先提取子程序，例如提取出错的函数，目的是减少输入量，集中以提高准确性
  * 接着 Syntax Prompt Generator 根据提供的一些信息，例如编译选项、编译报错信息等生成 prompt；
  * 然后，交由 LLMC 进行修复，由 Syntax Oracle （例如编译器）验证是否通过；
  * 可重复以上步骤，直到完全修复。
* **语义修复阶段：**
  * Semantic Prompt Generator 同样，根据题目描述、测试样例等等信息生成 prompt；
  * 交由 LLMC 进行修复，由 Semantic Oracle（例如 OJ 的评测）验证是否通过；
  * 同样可以多次迭代，并且如果生成多个候选，且都通过所有测试用例，考虑返回相对于原始程序具有**最小标记编辑距离**的程序。

## Demo

为了迎合做出一个 demo，快速上线代码修复模块的需求，目前简化流程，以最小化的原则构建了极其精简的 API 和 grpc 模块，整体处理流程为：

* 通过 grpc 从后端接收所需信息；
* 将两阶段合并为一阶段，一次性输入问题描述、编译选项、目标语言、用户待修复程序，生成 prompt；
* 考虑到响应时间，经过测试单次调用 OenAI api 的响应时间在 4s 左右，如果多次调用，可能响应时间不可接受，因此暂时只调用一次，并且不加验证地直接返回。(暂时出于简化与后端的交互考虑)

> 由于服务器不可科学上网，采用 cloudfare 代理方案

以上即完成了一次非常简单的代码修复，初步对 100 个 c 语言程序进行了修复，首次修复率超过 90%，由此也可浅窥大模型强悍之处。

前端部分 TBD。

## 扩展

基于上面的最小可执行部件，可以像搭积木一样逐步向上扩展，以下为一些未来的构想：

- [ ] 实现原有的两阶段框架；
- [ ] 实现对输入程序的分割/子程序的提取；
- [ ] 对语法阶段 prompt 生成，添加编译报错信息（尤其是准确的定位）；
- [ ] 对语义阶段 prompt 生成，添加运行报错信息、历史提交及修复对比、标准程序或其它正确程序、测试样例等等；
- [ ] 针对不同语言定制不同 prompt 生成策略（包括所需传入的信息），以及不同的验证策略，例如仅验证 `python` 语法错误的修复并不方便；
- [ ] 关于与后端的交互，由于语法语义阶段的**验证**以及相关**信息**的获取需要**多次**从后端获取，检验时延是否可接受；
- [ ] 关于 api 的调用，为提高响应速度，如果要多次迭代，考虑是否有并行的可能；
- [ ] 如果并行，并且生成了多个修复结果，需要定义好的标记编辑距离以评估修复结果；
- [ ] 针对修复率在大规模数据集上的安全评测；
- [ ] 由修复率的评测结果进行针对性的改进；

此外，以下为 api 可能返回的结果，针对不同的情况也可考虑设计不同的策略：

* 需要更多信息：询问有关程序行为的更多信息，以识别错误；
* 未发现错误：未发现错误，并表示程序工作正常；
* 提供的正确修复程序：为正确的错误提供正确的修复程序；
* 尝试修复其他问题：没有找到预期的错误，并尝试修复或建议其他不是真正错误的问题，或针对边缘情况进行调整；
* 提供修复但引入新错误：为目标错误提供正确的修复，但在其他地方引入新错误；
* 替代实现：不修复错误，但提供了一个可行的替代实现。

> 题外话，关于在 OJ 上线代码修复功能，不知是否与让学生通过 OJ 提高编程能力（包括 debug 能力）的初衷相违背，以及未来真的上线后有什么具体限制措施尚未可知，且观望吧。(doge)

## 参考资料

[Repairing Bugs in Python Assignments Using Large Language Models](https://arxiv.org/abs/2209.14876)

[An Analysis of the Automatic Bug Fixing Performance of ChatGPT](https://arxiv.org/abs/2301.08653)

[Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)

[MACER: A Modular Framework for Accelerated Compilation Error Repair](https://github.com/purushottamkar/macer)

[DeepFix: Fixing Common C Language Errors by Deep Learning](https://paperswithcode.com/paper/deepfix-fixing-common-c-language-errors-by)

[QuixBugs: A multi-lingual program repair benchmark set based on the Quixey Challenge](https://jkoppel.github.io/QuixBugs/)

[HumanEval: Hand-Written Evaluation Set](https://github.com/openai/human-eval)

