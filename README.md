# AI-Driven Python Selenium BDD Framework

This enterprise-grade automation framework leverages AI to transform requirements into executable BDD tests. It features a robust `BasePage` architecture, multi-model AI routing, and seamless JIRA integration.

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python:** 3.10 or higher.
- **Dependencies:** Run `pip install -r requirements.txt`.
- **AI Configuration:** Update `config/ai.yaml` with your API keys (OpenAI, Gemini, or Groq).

### 2. Execution Commands

| Task | Windows (.bat) | Linux/Mac (.sh) |
| :--- | :--- | :--- |
| **AI Generation** | `scripts\ai_generate.bat` | `./scripts/ai_generate.sh` |
| **Run BDD Tests** | `scripts\run_bdd.bat` | `./scripts/run_bdd.sh` |
| **AI Quick Fix** | `scripts\ai_quick_fix.bat <file> "<error>"` | `./scripts/ai_quick_fix.sh <file> "<error>"` |
| **Allure Report** | `scripts\generate_allure.bat` | `./scripts/generate_allure.sh` |

---

## 🧠 AI Features Guide

### 1. Multi-Model Strategy & Free-Tier Support
The framework supports **Smart Routing** to optimize performance and cost. Configure this in `config/ai.yaml`:
- **OpenAI (Default):** Best for complex code generation.
- **Google Gemini:** Cost-effective for code reviews and documentation.
- **Groq (Llama 3):** Ultra-fast for assertions and simple logic.

### 2. AI Quick Fix & Assertions
- **Quick Fix:** Automatically debugs errors in Feature files, Step Definitions, or Page Classes.
- **AI Assert:** Use `execute_assert(condition, context)` in your steps for intelligent validation of complex UI states.

### 3. JIRA-to-BDD Flow
Include JIRA details in `requirements/user_story.txt` to fetch requirements directly:
```text
JIRA_KEY: ATH-123
JIRA_URL: https://your-domain.atlassian.net
```

---

## 🏗️ Architecture: Enhanced BasePage

All Page Objects must extend the `BasePage` class to leverage these reusable methods:

| Category | Reusable Methods |
| :--- | :--- |
| **Mouse Actions** | `click`, `double_click`, `right_click`, `hover`, `drag_and_drop` |
| **Input & Keys** | `enter_text`, `get_text`, `press_key`, `select_all_and_delete` |
| **JavaScript** | `js_click`, `scroll_to_element`, `js_execute` |
| **Dropdowns** | `select_by_visible_text`, `select_by_value`, `select_by_index` |
| **Reporting** | `take_screenshot`, `attach_screenshot_to_allure` |

---

## 🛠️ Implementation Steps for New Requirements

1.  **Define Requirement:** Add a new `.txt` file in the `requirements/` folder (or update `user_story.txt`).
2.  **Run AI Generation:** Execute `scripts/ai_generate.sh`. The AI will:
    - Search the **RAG Knowledge Base** for existing `BasePage` methods.
    - Generate a `.feature` file, Step Definitions, and a Page Class.
3.  **Review & Refine:** Use `scripts/ai_quick_fix.sh` if any generation errors occur.
4.  **Execute:** Run your tests using `scripts/run_bdd.sh` and view the Allure report.
