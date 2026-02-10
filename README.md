# AI-Driven Python Selenium BDD Framework (Enterprise Edition)

This framework integrates **Behavior-Driven Development (BDD)** with **Artificial Intelligence** to automate the entire testing lifecycle. It features JIRA automation, global code deduplication, and cross-platform support.

## Framework Architecture

The system uses a **Hybrid Page Object Model (POM)** enhanced by an AI engine that understands your domain through a local knowledge base.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **BDD Core** | Behave | Test case definition and execution |
| **Automation** | Selenium 4 | Web browser interaction |
| **AI Engine** | LLM Factory | Code generation and synchronization |
| **Context** | FAISS + RAG | Domain-specific knowledge injection |
| **Integrations** | JIRA & Git | Enterprise workflow automation |
| **OS Support** | Win/Linux/Mac | Cross-platform execution scripts |

---

## Key Enterprise Features

### 1. JIRA-to-Code Automation
Transform JIRA issues directly into executable code.
- **Input:** Provide a **JIRA ID** (e.g., `JIRA: PROJ-123`) in `requirements/user_story.txt`.
- **Fetch:** The framework pulls Summary, Description, Acceptance Criteria (AC), and Epic details.
- **Generate:** AI analyzes the ACs to generate feature files and robust Page Object methods.

### 2. Intelligent Global Deduplication
The AI engine acts as a "smart architect" to prevent redundant code.
- **Scan:** Scans all existing feature steps and page methods globally.
- **Reuse:** If a "Login" or "Navigation" flow already exists, the AI reuses those assets instead of duplicating them for new requirements.

### 3. Conditional Execution Toggles
Manage enterprise dependencies easily via `config/framework.yaml`.
- **Toggles:** Set `jira: enabled: false` or `git: enabled: false` to skip those integrations.
- **Robustness:** The AI engine intelligently ignores these methods and dependencies when disabled, ensuring the framework runs smoothly in any environment.

### 4. Robust Requirement Parsing
The `user_story.txt` parser is built for real-world requirements.
- **Multi-line Support:** Seamlessly handles multi-line Summary, Description, and Acceptance Criteria without errors.
- **Variable Mapping:** Automatically maps test data to generated methods.

---

## Execution Guide

### Environment Setup
1.  **Install Python:** Python 3.10 or higher.
2.  **Dependencies:** Run `pip install -r requirements.txt`.
3.  **AI Configuration:** Update `config/ai.yaml` with your API keys.

### Execution Commands
| Task | Windows (.bat) | Linux/Mac (.sh) |
| :--- | :--- | :--- |
| **AI Generation** | `scripts\ai_generate.bat` | `./scripts/ai_generate.sh` |
| **Run Tests** | `scripts\run_bdd.bat` | `./scripts/run_bdd.sh` |
| **Allure Report** | `scripts\generate_allure.bat` | `./scripts/generate_allure.sh` |

---

## Technical & Hardware Requirements

- **Hardware:** Minimum 8GB RAM (16GB for local RAG) and a Dual-core CPU.
- **Drivers:** Latest Chrome, Firefox, or Edge with corresponding WebDrivers.
- **AI Access:** Valid API keys for cloud providers or local Ollama instance.

For a detailed technical blueprint, refer to the `MASTER_FRAMEWORK_PROMPT.md`.
