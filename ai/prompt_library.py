class PromptLibrary:
    CODE_REVIEW_PROMPT = """
    Review the following Python Selenium code for:
    1. PEP8 compliance.
    2. Selenium anti-patterns (e.g., hard sleeps, missing waits).
    3. Duplicate logic.
    4. Security concerns.
    
    Code:
    {code}
    
    Output the review in Markdown format.
    """

    METHOD_SUGGESTION_PROMPT = """
    Given the following page description or element, suggest a Selenium Page Object method in Python:
    Description: {description}
    
    Provide only the method code.
    """

    # Enhanced Prompts for Automated Generation
    
    PAGE_METHOD_GENERATION_PROMPT = """
    You are an expert Automation Architect. Generate a Python Page Object method for a Selenium framework.
    
    CONTEXT FROM KNOWLEDGE BASE:
    {rag_context}

    CONTEXT:
    - Base Class Methods Available: click(locator), enter_text(locator, text), get_text(locator), is_displayed(locator), open_url(url)
    - ALL EXISTING PAGE METHODS IN FRAMEWORK: {existing_methods}
    - Target Action: {action_description}
    
    REQUIREMENTS:
    1. Use the existing BasePage methods.
    2. IMPORTANT: Scan 'ALL EXISTING PAGE METHODS IN FRAMEWORK'. If a method for this functionality (e.g., login, logout, add_to_cart) already exists anywhere in the framework, return ONLY the comment: # Use existing method: [method_name]
    3. Do NOT recreate logic that already exists. Prioritize global reuse.
    4. Use domain knowledge from the Knowledge Base to handle complex logic or specific selectors if provided.
    5. Otherwise, generate a clean, robust Python method.
    6. Return ONLY the code or the comment.
    """

    STEP_DEFINITION_GENERATION_PROMPT = """
    You are an expert BDD Engineer. Generate Behave step definitions in Python.
    
    CONTEXT:
    - Feature Step: {step_text}
    - Existing Step Definitions: {existing_steps}
    - Page Object Methods Available: {page_methods}
    
    REQUIREMENTS:
    1. Use @given, @when, or @then decorators appropriately.
    2. Use the provided Page Object methods where possible.
    3. If a matching step already exists in 'Existing Step Definitions', return "# Step already exists".
    4. Return ONLY the Python code for the step definition.
    """

    FEATURE_GENERATION_PROMPT = """
    You are an expert QA Analyst. Generate a Gherkin (.feature) file based on the following requirement.
    
    CONTEXT FROM KNOWLEDGE BASE:
    {rag_context}

    REQUIREMENT:
    {requirement_text}
    
    EXISTING STEPS IN FRAMEWORK:
    {existing_steps}
    
    REQUIREMENTS:
    1. Generate a comprehensive Feature file with multiple Scenarios covering ALL Acceptance Criteria.
    2. Use standard Gherkin syntax (Feature, Scenario, Given, When, Then).
    3. IMPORTANT: Review 'EXISTING STEPS IN FRAMEWORK'. Reuse these exact steps for common flows (e.g., Login, Logout, Navigation) instead of creating new ones.
    4. Incorporate the provided Test Data where applicable.
    5. Use the Knowledge Base context to ensure domain-specific terminology and rules are followed.
    6. Return ONLY the Gherkin content.
    """

    SYNC_STEP_DEFINITION_PROMPT = """
    You are an expert BDD Engineer. Update the following step definition to match the new step text.
    
    NEW STEP TEXT: {new_step_text}
    EXISTING CODE: {existing_code}
    PAGE METHODS AVAILABLE: {page_methods}
    
    REQUIREMENTS:
    1. Update the decorator and the method logic to match the new step intent.
    2. Leverage existing Page Object methods.
    3. Return ONLY the updated Python code for the step definition.
    """

    LOGIC_GENERATION_PROMPT = """
    You are an expert Automation Architect. Generate robust Python Selenium logic based on the following prompt.
    
    PROMPT: {user_prompt}
    CONTEXT:
    - Base Class Methods: click, enter_text, get_text, is_displayed, open_url
    - Existing Page Methods: {existing_methods}
    
    REQUIREMENTS:
    1. Generate a complete, reusable Python method.
    2. Follow Page Object Model best practices.
    3. Return ONLY the Python code.
    """

    JIRA_REQUIREMENT_PROMPT = """
    You are an expert Test Architect. Convert the following JIRA Issue data into a structured requirement for automation.
    
    JIRA DATA:
    {jira_data}
    
    REQUIREMENTS:
    1. Extract the core User Story.
    2. List all Acceptance Criteria clearly.
    3. Identify Test Scenarios from the description and linked issues.
    4. Consider the context from the Parent Epic if provided.
    5. Format the output as a clean text requirement suitable for BDD generation.
    """
