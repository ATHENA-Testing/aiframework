# AI-Enabled Python Selenium BDD Hybrid Automation Framework

This document outlines the design, setup, and usage of a production-ready, enterprise-grade AI-enabled Python Selenium BDD Hybrid Automation Framework. This framework is designed to be static, reusable, and highly configurable via YAML files, allowing for seamless integration and adaptation across multiple projects.

## Framework Philosophy

Our core philosophy is **"Framework First, AI Second"**. This means the automation framework is robust and fully functional even with AI capabilities disabled. AI is treated as a plug-in capability, enhancing the framework's efficiency and intelligence without being its central dependency. The framework emphasizes **Config-Driven Behavior**, where changing AI models, versions, or providers requires zero code changes, relying solely on external YAML configurations. We also prioritize **Clean Separation of Concerns**, isolating AI logic from core automation logic, and ensuring **Enterprise Scalability** for multi-project readiness and CI/CD friendliness. Finally, **Local Execution** is a key principle, removing mandatory cloud dependencies for AI operations.

## Architecture Diagram

```mermaid
graph TD
    A[User/CI/CD] --> B(run_bdd.sh)
    B --> C{Framework Core}
    C --> D[config/framework.yaml]
    C --> E[config/environments.yaml]
    C --> F[features/]
    F --> G[features/steps/]
    G --> H[pages/]
    H --> I[base/]
    I --> J[utils/logger.py]
    I --> K[base/driver_manager.py]
    I --> L[base/waits.py]
    C --> M{AI Module}
    M --> N[config/ai.yaml]
    M --> O[ai/model_registry.yaml]
    M --> P[ai/llm_provider.py]
    M --> Q[ai/ai_executor.py]
    M --> R[ai/prompt_library.py]
    M --> S[ai/ai_code_review.py]
    M --> T[ai/ai_generator.py] %% Added AI Generator
    C --> U[data/test_data.json]
    C --> V[keywords/common_keywords.py]
    C --> W[reports/]
    W --> X[Allure Reports]
    S --> Y[review/ai_review_report.md]
```

## One-Time Setup

To set up the framework, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ai-bdd-automation-framework
    ```

2.  **Install dependencies:**
    It is highly recommended to use a virtual environment.
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure `config/framework.yaml`:**
    Adjust browser, headless mode, timeouts, and other general framework settings.

4.  **Configure `config/environments.yaml`:**
    Define URLs and credentials for different testing environments (e.g., staging, production).

5.  **Configure `config/ai.yaml` (if using AI features):**
    Set `enabled` to `true`, choose an `mode` (assist, generate, review), `provider`, `model`, and `version`. Provide necessary API keys or endpoints.

## Running Tests

Tests are executed using Behave. The framework provides cross-platform scripts for both Linux/Mac and Windows.

### On Linux/Mac:
1.  **Activate virtual environment:** `source venv/bin/activate`
2.  **Run tests:** `./scripts/run_bdd.sh`
3.  **Generate Allure Report:** `./scripts/generate_allure.sh`

### On Windows:
1.  **Activate virtual environment:** `venv\Scripts\activate`
2.  **Run tests:** `scripts\run_bdd.bat`
3.  **Generate Allure Report:** `scripts\generate_allure.bat`

## AI-Powered Intelligent Automation Engine

This framework includes a state-of-the-art AI engine that handles the entire lifecycle of automation development, from requirements to iterative code synchronization.

### 1. Requirement-to-Code Generation
Process user stories, acceptance criteria, and test data into complete automation suites.
- **Define Requirements:** Add a `.txt` file to `requirements/` using the provided template.
- **Run Generator:** 
  - **Linux/Mac:** `./scripts/ai_generate.sh`
  - **Windows:** `scripts\ai_generate.bat`
  The AI will create the `.feature` file, step definitions, and Page Object methods.

### 2. Iterative Feature Synchronization
If you update a step in an existing `.feature` file, the framework detects the change and synchronizes your code.
- **Update Feature:** Modify any step text in your `.feature` file.
- **Sync:** Run `./scripts/ai_generate.sh`. The AI will generate the new step definition and corresponding Page Object methods, while attempting to reuse existing logic where possible.

### 3. In-Code "Smart Prompts"
Generate complex Selenium logic directly inside your Page Classes using natural language.
- **Write Prompt:** In any `.py` file under `pages/`, add a comment like:
  `# AI: Create a method to handle a complex dynamic table with pagination and search`
- **Generate:** Run `./scripts/ai_generate.sh`. The AI will replace the comment with fully functional Python Selenium code.

### 4. RAG-Enabled Knowledge Base
The framework uses **Retrieval-Augmented Generation (RAG)** to provide domain-specific context to the AI model.
- **Add Knowledge:** Place `.txt` or `.md` files in the `knowledge_base/` directory. These files can contain domain rules, preferred selectors, business logic, or common workflows.
- **Automatic Context:** When generating features or code, the AI engine automatically searches your knowledge base for relevant information and includes it in the prompt to ensure the output is accurate and follows your project's specific standards.
- **Index Rebuild:** The vector index is automatically rebuilt every time you run the generation script to include your latest documentation.

### 5. How to Enable
Ensure `config/ai.yaml` has:
```yaml
ai:
  enabled: true
  mode: generate
```

## Enabling / Disabling AI

AI capabilities are controlled via `config/ai.yaml`.

To **enable** AI, set `enabled: true` and choose a `mode`:

```yaml
ai:
  enabled: true
  mode: assist # off | assist | generate | review
  provider: openai
  model: gpt-4
  version: latest
  api_key: "YOUR_OPENAI_API_KEY"
```

To **disable** AI, set `enabled: false` or `mode: off`:

```yaml
ai:
  enabled: false
  mode: off
```

## Switching Models & Versions

Model configuration is externalized in `config/ai.yaml` and `ai/model_registry.yaml`.

To switch models or versions, simply update `config/ai.yaml`:

```yaml
ai:
  provider: ollama
  model: mistral
  version: 7b
  ollama:
    host: "http://localhost:11434"
```

The `ai/model_registry.yaml` file lists supported models and their available versions for each provider.

## Offline AI Usage (Ollama)

For offline AI capabilities, configure `config/ai.yaml` to use the `ollama` provider and ensure Ollama is running locally.

1.  **Install Ollama:** Follow instructions on [Ollama's official website](https://ollama.ai/).
2.  **Download a model (e.g., Mistral):**
    ```bash
    ollama run mistral
    ```
3.  **Configure `config/ai.yaml`:**
    ```yaml
ai:
  enabled: true
  mode: review
  provider: ollama
  model: mistral
  version: latest
  ollama:
    host: "http://localhost:11434" # Default Ollama host
    ```

## CI/CD Usage

Integrate the framework into your CI/CD pipeline by ensuring the virtual environment is activated and `run_bdd.sh` is executed. Allure reports can be published to an Allure server or generated as static HTML.

Example GitLab CI/CD snippet:

```yaml
stages:
  - test
  - report

run_tests:
  stage: test
  script:
    - python3.10 -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - ./scripts/run_bdd.sh
  artifacts:
    paths:
      - reports/allure-results/
    expire_in: 1 day

generate_report:
  stage: report
  image: "frankescobar/allure-docker-service"
  script:
    - allure generate reports/allure-results --clean -o reports/allure-html
    - echo "Allure report generated in reports/allure-html"
  artifacts:
    paths:
      - reports/allure-html/
    expire_in: 1 week
  dependencies:
    - run_tests
```

## Best Practices

*   **Page Object Model (POM):** Maintain a clean separation of UI elements and interactions in `pages/`.
*   **Keyword-Driven:** Utilize `keywords/` for reusable, high-level actions.
*   **Data-Driven:** Store test data in `data/` (e.g., `test_data.json`) and parameterize tests.
*   **Base Classes:** Place all common Selenium logic in `base/base_page.py` to avoid duplication.
*   **AI Code Review:** Regularly run `ai/ai_code_review.py` to identify and fix issues like PEP8 violations, Selenium anti-patterns, and duplicate logic.
*   **AI Script Generation:** Use `./scripts/ai_generate.sh` to accelerate the creation of step definitions and page object methods.
*   **Logging:** Use the integrated logger (`utils/logger.py`) for comprehensive test execution logs.
*   **Configuration:** Centralize all configurations in `config/` for easy management and environment switching.

## References

*   [Behave Documentation](https://behave.readthedocs.io/en/latest/)
*   [Selenium WebDriver](https://www.selenium.dev/documentation/)
*   [Allure Report](https://allurereport.org/docs/)
*   [Ollama Official Website](https://ollama.ai/)
