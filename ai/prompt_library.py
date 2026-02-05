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
    - Existing Page Methods: {existing_methods}
    - Target Action: {action_description}
    
    REQUIREMENTS:
    1. Use the existing BasePage methods.
    2. Do NOT recreate logic that already exists in 'Existing Page Methods'.
    3. Use domain knowledge from the Knowledge Base to handle complex logic or specific selectors if provided.
    4. If the action can be performed by an existing method, return a comment saying "# Use existing method: [method_name]".
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
    
    REQUIREMENTS:
    1. Generate a comprehensive Feature file with multiple Scenarios covering ALL Acceptance Criteria.
    2. Use standard Gherkin syntax (Feature, Scenario, Given, When, Then).
    3. Incorporate the provided Test Data where applicable.
    4. Use the Knowledge Base context to ensure domain-specific terminology and rules are followed.
    5. Return ONLY the Gherkin content.
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
