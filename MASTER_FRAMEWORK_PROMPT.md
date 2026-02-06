# Master System Prompt: AI-Driven Python Selenium BDD Framework

## Objective
Generate a production-ready, enterprise-grade AI-Enabled Python Selenium BDD Hybrid Automation Framework that is static, reusable, and configurable.

## Technical Stack
- **Language:** Python 3.10+
- **BDD Framework:** Behave
- **Automation Tool:** Selenium 4.x
- **Design Pattern:** Page Object Model (POM) + Hybrid (Keyword & Data Driven)
- **AI Engine:** Custom LLM Provider Factory (OpenAI, Azure, Ollama)
- **RAG System:** FAISS Vector DB + Sentence-Transformers (all-MiniLM-L6-v2)
- **Reporting:** Allure Reports
- **OS Support:** Cross-platform (Windows .bat, Linux/Mac .sh)

## Hardware & Environment Requirements
- **CPU:** Minimum Dual-core (Quad-core recommended for local RAG indexing)
- **RAM:** 8GB Minimum (16GB recommended for local LLM/RAG operations)
- **Disk Space:** 2GB for framework and dependencies
- **Internet:** Required for cloud LLM providers (OpenAI/Azure); optional for local providers (Ollama)
- **Drivers:** Chrome/Edge/Firefox installed with matching WebDriver

## Core Capabilities to Generate

### 1. AI End-to-End Generation (Requirement-to-Code)
- **Input:** Text files in `requirements/` containing User Stories, Acceptance Criteria, and Test Data.
- **Output:** Automatic generation of `.feature` files, `steps.py` definitions, and `page.py` methods.
- **Logic:** Full coverage of all ACs, mapping steps to intelligent page actions.

### 2. Iterative Synchronization
- **Trigger:** Changes in existing `.feature` files.
- **Action:** LLM detects updated step text, overrides old step definitions, and updates Page Object methods to match the new intent.

### 3. In-Code "Smart Prompts"
- **Syntax:** `# AI: [natural language prompt]` inside Page Classes.
- **Action:** Processor replaces comments with robust Selenium Python logic, leveraging base class utilities and existing methods.

### 4. RAG-Enabled Knowledge Base
- **Storage:** `knowledge_base/` folder for `.txt` and `.md` files.
- **Processing:** Chunking, tokenization, and vector indexing via FAISS.
- **Usage:** Semantic search injects domain-specific context (rules, selectors, workflows) into LLM prompts for high-accuracy generation.

### 5. Enterprise Utilities
- **DriverManager:** Singleton pattern for cross-browser support.
- **BasePage:** Wrapper for Selenium actions with explicit waits and logging.
- **Config:** YAML-based configuration for environments and AI settings.
- **Reporting:** Automatic screenshot capture on failure and Allure integration.

## Implementation Guidelines
- Use `os.path.join` for all pathing to ensure cross-platform compatibility.
- Implement strict error handling and logging.
- Prioritize code reuse by checking existing methods before generating new ones.
- Ensure all generated code follows PEP 8 standards.
