# 钢智灵枢——面向钢铁仓储的多模态AI智能决策平台

## 项目说明
钢智灵枢以多模态AI为核心，通过钢卷智能感知、仓储状态分析和天车智能决策，实现钢铁仓储“感知—分析—决策—执行—反馈”的智能闭环。

## 软件界面
当前版本按照项目演示视频中的业务界面重新实现，包含：
- 查看仓储状态
- 钢卷AI识别
- 信息确认
- 创建任务
- 智能调度
- 执行状态
- 异常处理
- 任务完成与状态更新

## 运行环境
建议 Windows + Python 3.11 64-bit。

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## YOLO26 权重
将 `yolo26n.pt` 放入：

```text
models/yolo26n.pt
```

当前工程会优先加载该权重；未提供权重时保留 OpenCV 兜底检测流程。

## 注意
`ppo_agent.py` 当前为调度策略接口/原型，并非经过训练的 PPO 神经网络权重；`yolo26_lie.py` 当前为 YOLO26 与李代数、超图、粒球模块的工程融合接口。不要将其描述为已经完成专门训练的 YOLO26-Lie 或 PPO 模型。
