from setuptools import setup, find_packages

setup(
    name="ai-bdd-automation-framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "behave",
        "pyyaml",
        "webdriver-manager",
        "allure-behave",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "ai-review=ai.ai_code_review:main",
        ],
    },
)
