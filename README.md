Prompt Optimization using Local LLM to Reduce Cloud LLM Cost

Technical Overview:
This repository contains a modular 3-stage AI engineering pipeline designed to reduce the operational costs of high-end LLMs (like Grok-1 or GPT-4). The system implements a Small-to-Large Model Pipeline where a local SLM (Phi-3:mini) acts as an intelligent "Compressor" to optimize user prompts before they are sent to an expensive cloud-based API.

The Problem:
Cloud LLM costs are calculated by token count. Raw user queries are often verbose, unorganized, and redundant, leading to significantly higher API costs without improving response quality.

The Solution:
A 3-stage automated pipeline:

1. Ingestion: Batch processing of raw queries from JSON sources.
2. Optimization: A local LangGraph node uses Phi-3-mini to rewrite the prompt into a concise, professional instruction.
3. Execution: The optimized prompt is sent to the Grok API, significantly reducing the input token overhead.

Dataset Details:
• No. of Rows: 6648
• No. of Columns: 2
• Queries processed at a time in batch size : 50
• Source of Dataset: Hugging Face
• File Format: json
• Datasource : https://huggingface.co/datasets/mteb/fiqa/viewer/queries

System Architecture:
The Technical Workflow:

1. Raw Ingestion: The system accepts a raw, verbose user query.

2. Local Optimization (Phi-3 Mini): The query is processed locally via Ollama.
   The SLM identifies the core intent and removes conversational noise.
   Output: A high-density, token-reduced version of the original prompt.

3. Cloud Execution (Grok API):
   The Optimized Prompt is dispatched to the xAI Grok endpoint.
   The API generates a high-reasoning response based on the "surgical" input.

4. Final Output: The system pairs the original query, optimized prompt, and final response into a structured report.

Project structure:
Project Structure:
.
├── data/
│   └── queries.json
├── optimizer/
│   ├── optimizer_node.py
│   ├── prompt_templates.py
│   └── token_utils.py
├── stages/
│   ├── batch_stage1.py
│   ├── batch_stage2_safety_net.py
│   └── batch_stage3.py
├── graph.py
├── requirements.txt
└── README.md

Performance Showcase:
By leveraging local SLMs for pre-processing, we achieved substantial token savings while maintaining high-quality outputs.

---

| Metric Original (Raw) | Optimized (Phi-3) | Efficiency Gain |      

| Avg. Query Length | 154 chars | 68 chars ~55% Reduction |             

| Avg. Token Cost | High ($$$) Optimized | ($) Cost-Effective |


Installation & Setup:
Prerequisites
• Ollama installed on your machine.
• Python 3.12+ environment.

1. Clone & Environment
   git clone
   cd
   pip install -r requirements.txt

2. Local Model Setup
   ollama pull phi3:mini

3. API Configuration
   Create a .env file in the root directory:
   GROK_API_KEY=your_api_key_here

Run the pipeline stages sequentially:
#Start the optimization and execution pipeline
python stages/batch_stage1.py
python stages/ batch_stage2_safety_net.py
python stages/batch_stage3.py

Hardware Requirements & Engineering Constraints:
Environment Specifications:
• Operating System: Ubuntu 24.04 LTS
• Local Inference Engine: Ollama (serving Phi-3-mini)
• Compute: INTEL CORE I5
• Memory: 16GB RAM (10GB Assigned to Virtual Machine )

Scale & Throughput Note:
While the architecture is designed to handle the full 6,648-row FIQA dataset, processing was intentionally limited by local hardware constraints, specifically a VM environment assigned 10GB of RAM. To maintain system stability and manage the memory overhead of running local inference (Ollama/Phi-3) alongside the execution pipeline, testing was performed in iterative batches of 5, 20, and 50 queries across different stages. This modular approach allowed for logic verification and safety-net benchmarking without exceeding the physical hardware limits of the laptop, ensuring the system remains architecturally ready for full-scale deployment on high-performance GPU instances.



