# MASTER FRAMEWORK PROMPT: AI-Driven Python Selenium BDD

This document serves as the technical blueprint for the AI Intelligent Automation Engine. It defines the core principles, architecture, and AI-driven workflows for generating enterprise-grade automation code.

---

## 🏗️ Core Principles

### 1. Enhanced BasePage Architecture
- **Inheritance:** All Page Objects MUST extend the `BasePage` class.
- **Reusability:** Prioritize using existing `BasePage` methods (e.g., `click`, `enter_text`, `js_click`, `press_key`, `take_screenshot`).
- **Encapsulation:** Locators and methods are encapsulated within Page Objects, following the Page Object Model (POM).

### 2. Multi-Model AI Strategy & Smart Routing
- **Generation:** Use high-performance models (e.g., `gpt-4o`) for complex code generation and synchronization.
- **Review:** Use cost-effective models (e.g., `gemini-1.5-flash`) for automated code reviews and PEP8 compliance.
- **Assertion:** Use fast, low-latency models (e.g., `groq/llama3-8b`) for intelligent assertions and validation of UI states.
- **Robustness:** Implement exponential backoff and model fallback (e.g., `gpt-4o` -> `gpt-4o-mini` -> `gpt-3.5-turbo`) to handle rate limits (429 errors).

### 3. JIRA-Driven Requirements & RAG
- **JIRA Integration:** Support for parsing JIRA keys from `user_story.txt` to fetch requirements directly.
- **RAG Engine:** Semantic search across `knowledge_base/` to inject project-specific rules, selectors, and existing `BasePage` methods into LLM prompts.
- **Deduplication:** AI MUST scan existing feature steps and page methods globally to reuse framework assets before generating new code.

---

## 🛠️ AI-Driven Workflows

### 1. AI Generation & Synchronization
- **Input:** User requirements (text files or JIRA).
- **Process:** AI generates Gherkin features, step definitions, and page classes.
- **Sync:** Automatically updates code when `.feature` steps are modified.

### 2. AI-Driven Debugging & Assertions
- **Quick Fix:** Automated debugging utility (`ai_quick_fix.py`) with cross-platform scripts (`ai_quick_fix.bat`, `ai_quick_fix.sh`) that analyzes errors in any framework file and suggests code corrections.
- **AI Assert:** Intelligent validation of complex test conditions using LLM reasoning.
- **AI Review:** Automated code review for PEP8 compliance and Selenium best practices.

---

## 📋 Implementation Guidelines

### 1. Page Object Methods
- Use `self.click(locator)` instead of `self.driver.find_element(*locator).click()`.
- Use `self.enter_text(locator, text)` for all input fields.
- Use `self.press_key(locator, Keys.ENTER)` for keyboard actions.
- Use `self.take_screenshot(name)` for visual evidence in reports.

### 2. Error Handling & Robustness
- Implement global try-except blocks with smooth exit mechanisms.
- Use AI-assisted error reporting to provide clear fixes for automation failures.
- Ensure all dependencies (JIRA, Git) are conditionally executed based on `framework.yaml`.
