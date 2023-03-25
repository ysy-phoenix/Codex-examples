## Repairing Bugs in Python Assignments Using Large Language Models

> 这是调研时候阅读的第一篇，因此整理得细致一些。

### Introduction

MMAPR feature：多模态提示、迭代查询、基于测试用例的少样本选择和基于结构的程序分块。

> Few-shot 技术旨在通过利用很少的标记数据来训练模型，以在相似但未见过的情况下进行准确的预测。

三个挑战：

- 只有唯一正确性标准(例如测试用例）
  
  > 但是可以利用多种来源的信息：错误程序、标准解答代码、需要通过的测试用例、用自然语言描述任务、甚至编译器提供的信息)；
- 需防止 LLMC 生成的代码过多，或者对程序中没有错误的部分进行更改；
- 将 LLMC 作为黑盒，需采用基于提示的学习(**prompt-based learning**)

一些手段：

- 通过检索其它学生有类似错误的程序(以及最终修正)，在 prompt 中添加与任务相关的示例。通过计算相似性度量以识别这样的程序。
- 为了减少由语法错误引起的更改(这些错误本应有相对**简单**的修复)，通过程序的结构来**提取子程序**作为 LLMC 的输入，减少暴露给 LLMC 的代码，来表明**偏好少的编辑**。

效果(与 BIFI 和 Refactory 的结合进行对比)：

- 首先，总之效果非常好，修复率高，平均编辑距离少；
- 特别地，迭代查询和少样本技术对修复率提高有帮助(后者提升更大)；
- 此外，删除提取子程序会导致平均编辑距离的提高；
- 最后，不同多模态具有不同性能，需要组合一获得最佳性能。

> 较小的编辑距离可以帮助学生理解对自己错误的修复。

### Background

- 大型语言模型（LLM）可以看作是单词序列上的概率分布。这种分布是使用具有大量参数的深度神经网络来学习的。
- 与传统的有监督机器学习相比，LLM 已被证明对少数甚至零样本学习有效。
- 在这种少样本（或零样本）学习的情况下，LLM 通常使用所谓的基于提示的学习。提示是一个文本模板，可以作为 LLM 的输入，以获得迭代预测的下一个序列，称为生成。提示通常由一个**查询**和可能的零个或多个任务示例(**shots**)组成。
- 提示可以包含任何可以以文本格式捕获的内容。特别是，多模式提示是那些包含**不同输入模式**的提示，如自然语言、代码和数据。
- 一个重要的超参数是 temperature，它控制着我们对不太可能的完井进行采样的程度。

### METHODOLOGY

#### 基础架构：

- 错误程序首先进入语法修复阶段
  
  - 从有语法错误的原始程序中提取子程序；
  - 每个子程序被送到语法提示生成器，该生成器生成多个面向语法的提示；
  - 然后，LLMC 生成修复候选，这些候选由语法预测器进行验证；
  - 重复以上过程，直到删除所有语法错误为止；
  - 没有语法错误的程序会进入语义阶段；
- 语义修复阶段
  
  - 语义提示生成器来生成面向语义的提示；
  - 如果可以访问其它学生的提交历史，MMAPR 也可以在这些提示中添加一些样本；
  - 通过基于测试套件的语义预测器进行验证；
  - 如果多个候选满足所有测试用例，则 MMAPR 返回相对于学生的原始 Bugy 程序具有最小标记编辑距离的程序。

#### Syntax Phase

> 使用编译器或解释器作为语法预测器。

虽然语法提示生成器可以直接在提示中包含原始程序，但是这样做可能会导致**虚假的编辑**， 而这些编辑实际上并不是解决语法错误所必需的。
引入了一个称为程序块的组件，通过减少提示中包含的代码量来缓解这一问题。

##### Program Chunking

对于错误程序中的每个语法错误，chunker 提取一个子行，其中包含

1. oracle 报告的语法错误位置
2. 最近的包含控制流语句。

换句话说，chunker 首先识别与语法错误行具有相同或较大缩进级别的相邻代码。
然后，如果代码块包含与控制流相关的关键字，例如 `if` 和 `elif`，则MMAPR会确保相应的关键字
（例如 `elif` 或 `else`）也在块中。然后将该程序块提供给语法提示生成器。

##### Syntax Prompt Generator:

语法提示生成器生成两个（多模态）提示，一个包含语法错误消息，另一个不包含。
由于语法预测器是可用的，不需要为所有程序选择一个提示模板，而是使用两个提示查询 LLMC，从每个生成中提取代码部分，
通过替换与当前程序块对应的行将其合并到原始程序中，然后依靠语法预测器过滤掉无效的修复。

迭代查询允许修复多个空间独立的语法错误。

#### Semantic Phase

> 使用测试套件（由输入和预期输出组成）作为语义预测器。

##### Semantic Prompt Generator

利用编程任务具有的一些特点：

1. 任务的自然语言描述；
2. 一组测试用例；
3. 同行的解答程序；

语义提示生成器将语法有效的程序、自然语言的任务描述和提供的测试用例作为输入。
然后，生成器生成具有这些信息的不同组合的提示。

最终返回具有最小基于标记的(token-based)编辑距离的修复程序。

##### Few-Shot Learning

给定由 MMAPR 的语法阶段生成的候选程序，寻找三个最**相似**的 $p$ 及其相关的正确版本 $p^{\prime}$($p$ 是 $p^{\prime}$ 的历史版本), 以作为样本包含在由语义提示生R成器生成的 LLMC 提示中。

定义如果两个程序导致相似的测试执行结果，那么它们是相似的。为程序 $p$ 定义了一个测试执行向量，
该向量捕获测试失败为 $T_p\in \mathcal{B}_n = (t_0，\cdots，t_n)$，其中 $n$ 是测试用例的数量，$t_i$ 是第 $i$ 个测试的失败状态的布尔值。将 $p_1$ 和 $p_2$ 之间的相似性函数定义为 $1−HAMMING(T_{p_1}，T_{p_2})$，$HAMMING$ 是两个向量之间的归一化汉明距离。

### Evaluation

选择 OpenAI 的 Codex 作为 LLMC。其他模型，如Codex Edit，表现不佳。根据初步实验，将 temperture 设置为0.8。

评估结论大体可参见先前 Introduction 中效果描述，另总结如下：

* MMAPR 修复率更高，即使没有用 few-shot）(86.71% vs 67.13%)，平均编辑距离更少（31.40 vs 42.50）；
* 再利用 few-shot 提高到 96.50%，但对平均编辑距离没有帮助(31.49)；
* BIFI 因为 lexer 无法修复其中的 17/286 个程序，而 MMAPR 基于提示的策略让其对输入没有任何限制；
* BIFI在修复难度较低的程序中的小语法错误方面非常有效，并且与 MMAPR 相比，以更小的平均标记编辑距离（1.82 vs 2.18）进行修复
  > 未来一个有趣方向是将 BIFI 与 MMAPR 结合起来，因为修复是可以互补的。在这种情况下，Codex 可以专注于生成更复杂的修复，而 BIFI 可以专注于对更简单的任务进行小的编辑，例如字符串中缺少一个引号。
* 程序分块可以减少平均标记编辑距离；
* 迭代查询，将关注点分为两个阶段会使整体修复率从 82.87% 提高到 86.71%，略微增加平均令牌编辑距离（30.29 到 31.40）；
* 多模态，提供 程序+诊断+描述+测试结构 最有效；
* BIFI + Refactory 的组合未必效果好，比如前者删除包含语法错误的语句进行修复，会给后者进行语义错误修复带来挑战。

## An Analysis of the Automatic Bug Fixing Performance of ChatGPT

> 这篇主要讲 ChatGPT，由于后面是基于 CodeX 的，因此只做简要总结一些结论。

* ChatGPT 所获得的结果在性能上与 Codex 相似，并且优于标准 APR 方法；(基于 QuixBugs 数据集)
* ChatGPT 在修复错误时似乎有相对较高的差异；(但是对于用户来说，这意味着多次执行请求可能会有所帮助）
* ChatGPT 回答有以下几种
  
  * 需要更多信息：询问有关程序行为的更多信息，以识别错误；
  * 未发现错误：未发现错误，并表示程序工作正常；
  * 提供的正确修复程序：为正确的错误提供正确的修复程序；
  * 尝试修复其他问题：没有找到预期的错误，并尝试修复或建议其他不是真正错误的问题，或针对边缘情况进行调整；
  * 提供修复但引入新错误：为目标错误提供正确的修复，但在其他地方引入新错误；
  * 替代实现：不修复错误，但提供了一个可行的替代实现。

## Evaluating Large Language Models Trained on Code

> 题为针对 LLMC 的评估，实际就是 OpenAI 对 Codex 的评估，挑重点摘录。

### Evaluation Framework

首先，不采用基于匹配的度量，而是考虑功能正确性(通过单元测试)。

定义 pass@k 度量：为每个问题生成 $k$ 个代码样本，如果有任何样本通过单元测试，则认为问题已解决。然而，以这种方式计算 pass@k 可能具有高的方差。因此，要评估 pass@k，为每个任务生成 $n\geq k$ 个样本（$n=200,\ k\leq 100$），计算通过单元测试的正确样本 $c\leq n$ 的数量，并计算无偏估计量。

$$
pass@k = \underset{problems}{\mathbb{E}}[1-\frac{\tbinom{n-c}{k}}{\tbinom{k}{n}}]
$$

直接计算这个估计量会直接导致非常大的数值不稳定性，需要简化表达式并逐项计算乘积。

评估了一组 164 个**手工编写**问题的功能正确性，称之为 HumanEval 数据集。(手工编写原因是模型是在 GitHub 上训练的，包含了各种来源问题的解决方案)

后面涉及了安全的测试环境、代码生成、docstring 生成，以及 Codex 的局限性。附录中还有关于细节的描述，还包括对未来的影响等等，考虑到目前关注点应该在 语法错误修复，暂且略过。

但是整体感受还是感觉大开眼界，可能看不懂，但是大受震撼.jpg。

## RELATED WORK

相关工作可就太多了，先不一一看了。列在这里可能留作参考，这里先找了三种编程语言的。

* Break-It-Fix-It: Unsupervised Learning for Program Repair（即第一篇提到的 BIFI，数据集是 Python）
* 37 Million Compilations: Investigating Novice Programming Mistakes in Large-Scale Student Data (基于 BlackBox 数据集对学生程序中的语法(编译)错误的研究，JAVA 语言)
* DeepFix: Fixing Common C Language Errors by Deep Learning（数据集为 C 语言）

## References

[MACER: A Modular Framework for Accelerated Compilation Error Repair](https://github.com/purushottamkar/macer)

[Break-It-Fix-It: Learning to Repair Programs from Unlabeled Data](https://github.com/michiyasunaga/bifi)

[DeepFix: Fixing Common C Language Errors by Deep Learning](https://paperswithcode.com/paper/deepfix-fixing-common-c-language-errors-by)

[QuixBugs: A multi-lingual program repair benchmark set based on the Quixey Challenge](https://jkoppel.github.io/QuixBugs/)

[HumanEval: Hand-Written Evaluation Set](https://github.com/openai/human-eval)

[HumanEval Community Code](https://paperswithcode.com/paper/evaluating-large-language-models-trained-on)

[HumanEval Dataset](https://paperswithcode.com/dataset/humaneval)

