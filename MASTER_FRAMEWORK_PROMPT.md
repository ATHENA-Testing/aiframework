# Master System Prompt: AI-Driven Python Selenium BDD Framework (Enterprise Edition)

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
- **Integrations:** JIRA (REST API), Git (GitPython)
- **OS Support:** Cross-platform (Windows .bat, Linux/Mac .sh)

## Hardware & Environment Requirements
- **CPU:** Minimum Dual-core (Quad-core recommended for local RAG indexing)
- **RAM:** 8GB Minimum (16GB recommended for local LLM/RAG operations)
- **Disk Space:** 2GB for framework and dependencies
- **Internet:** Required for cloud LLM providers; optional for local providers (Ollama)
- **Drivers:** Latest Chrome/Edge/Firefox installed with matching WebDriver

## Core Capabilities

### 1. Requirement-to-Code Generation (JIRA Integrated)
- **Input:** Text files in `requirements/` with User Stories or **JIRA IDs** (e.g., `JIRA: PROJ-123`).
- **Logic:** Automatically fetches deep story details (ACs, Epics, Scenarios) from JIRA.
- **Output:** Generates `.feature` files, step definitions, and Page Object methods with 100% AC coverage.

### 2. Intelligent Global Deduplication
- **Logic:** Scans all existing feature steps and page methods globally.
- **Action:** Prioritizes reusing existing framework assets over duplicating code. If a "Login" flow exists, the AI reuses it for all new requirements.

### 3. Iterative Synchronization & Smart Prompts
- **Sync:** Automatically updates code when `.feature` steps are modified.
- **Smart Prompts:** Replace `# AI: [prompt]` in Page Classes with robust, reusable Selenium logic.

### 4. Enterprise-Grade Robustness
- **Conditional Execution:** Toggles for JIRA and Git in `framework.yaml` to ignore dependencies when disabled.
- **Multi-line Parsing:** Robust parsing of User Stories, ACs, and Descriptions from text files.
- **Error Handling:** Global try-except blocks with smooth exit mechanisms to prevent framework crashes.

### 5. RAG-Enabled Knowledge Base
- **Storage:** `knowledge_base/` for domain documentation.
- **Usage:** Semantic search injects project-specific rules and selectors into LLM prompts.

## Implementation Guidelines
- Use `os.path.join` for cross-platform pathing.
- Implement strict error handling and logging.
- Prioritize code reuse by checking existing methods before generating new ones.
- Ensure all generated code follows PEP 8 standards.
