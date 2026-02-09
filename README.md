# AI-Driven Python Selenium BDD Framework

This enterprise-grade automation framework integrates **Behavior-Driven Development (BDD)** with **Artificial Intelligence** to automate the entire testing lifecycle. From requirement analysis to code generation and iterative maintenance, this framework leverages Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to deliver high-quality automation at scale.

## Framework Architecture

The system is built on a **Hybrid Page Object Model (POM)**. It combines the readability of Gherkin with the power of Python and Selenium, enhanced by an AI engine that understands your domain through a local knowledge base.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **BDD Core** | Behave | Test case definition and execution |
| **Automation** | Selenium 4 | Web browser interaction |
| **AI Engine** | LLM Factory | Code generation and synchronization |
| **Context** | FAISS + RAG | Domain-specific knowledge injection |
| **Reporting** | Allure | Detailed execution and failure analysis |
| **OS Support** | Win/Linux/Mac | Cross-platform execution scripts |

---

## Detailed Feature Guide

### 1. Requirement-to-Code Generation
This feature allows you to transform business requirements directly into executable code.
1.  **Input:** Place your requirement in `requirements/user_story.txt`. Include the User Story, Acceptance Criteria (AC), and Test Data.
2.  **Process:** The AI analyzes the ACs and generates a Gherkin `.feature` file.
3.  **Output:** It then auto-populates the corresponding step definitions and Page Object methods, ensuring 100% coverage of your requirements.

### 2. Iterative Feature Synchronization
Software requirements change frequently. This framework handles updates gracefully.
- If you modify a step in an existing `.feature` file (e.g., changing "I click login" to "I click the secure login button"), simply run the generator.
- The AI detects the change, identifies the old code, and **overrides** it with updated logic that reflects the new step text.

### 3. In-Code "Smart Prompts"
For complex logic that requires specific Selenium implementation, you can "chat" with the framework directly in your code.
- **Usage:** Add a comment like `# AI: Create a method to scrape all prices from the results table and return the average` in any page class.
- **Result:** The AI engine will replace that comment with a fully functional Python method, using the framework's `BasePage` utilities.

### 4. RAG-Enabled Knowledge Base
The framework doesn't just generate generic code; it learns your domain.
- **Knowledge Base:** Add documents to the `knowledge_base/` folder.
- **RAG Logic:** The system chunks these documents and stores them in a vector database. When generating code, it retrieves relevant snippets (like specific CSS selectors or business rules) to ensure the output is tailored to your application.

### 5. Consolidated Generation Summary (Response.txt)
After running the AI generation script, a consolidated report is created in `requirements/Response.txt`. This file contains:
- The generated **Gherkin Feature** steps.
- The corresponding **Step Definition** code blocks.
- The implemented **Page Class Methods** with logic ensuring 100% acceptance criteria coverage.

### 6. JIRA & Git Connectors
The framework now includes enterprise-grade connectors for seamless integration into your CI/CD and project management workflows.
- **JIRA Connector:** Located in `connectors/jira_connector.py`. Supports **API Token** and **SSO/OAuth** authentication. Configure your credentials in `config/framework.yaml`.
- **Git Connector:** Located in `connectors/git_connector.py`. Automates committing and pushing generated code to **GitHub** or **GitLab** repositories.

---

## Execution Guide

### Environment Setup
1.  **Install Python:** Ensure Python 3.10 or higher is installed.
2.  **Dependencies:** Run `pip install -r requirements.txt`.
3.  **AI Configuration:** Update `config/ai.yaml` with your API keys (OpenAI, Azure) or local endpoint (Ollama).

### Running on Windows (.bat)
| Task | Command | Description |
| :--- | :--- | :--- |
| **AI Generation** | `scripts\ai_generate.bat` | Processes requirements and syncs code. |
| **Run Tests** | `scripts\run_bdd.bat` | Executes all BDD features. |
| **Report** | `scripts\generate_allure.bat` | Compiles results into an Allure report. |

### Running on Linux/Mac (.sh)
| Task | Command | Description |
| :--- | :--- | :--- |
| **AI Generation** | `./scripts/ai_generate.sh` | Processes requirements and syncs code. |
| **Run Tests** | `./scripts/run_bdd.sh` | Executes all BDD features. |
| **Report** | `./scripts/generate_allure.sh` | Compiles results into an Allure report. |

---

## Technical & Hardware Requirements

To ensure smooth operation of the AI and RAG components, the following specifications are recommended:

- **Hardware:** Minimum 8GB RAM (16GB for local RAG indexing) and a Dual-core CPU.
- **Drivers:** Latest Chrome, Firefox, or Edge browser with corresponding WebDrivers.
- **AI Access:** Valid API keys for cloud providers or a running instance of Ollama for local execution.

For a detailed technical breakdown, refer to the `MASTER_FRAMEWORK_PROMPT.md` included in the root directory.
