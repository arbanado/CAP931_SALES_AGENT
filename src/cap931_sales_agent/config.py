"""
CAP 931 - Sales Agent Prototype
Configuration Module

This module loads environment variables and provides
central configuration settings for the multi-agent
sales assistant application.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_FILE = PROJECT_ROOT / ".env"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

DATA_DIR = PROJECT_ROOT / "data"


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(dotenv_path=ENV_FILE)


# ============================================================
# OPENAI CONFIGURATION
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1-mini",
)


# ============================================================
# WEB RESEARCH CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = 20

MAX_WEB_TEXT_CHARS = 15000

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; CAP931SalesAgent/1.0; "
    "+educational-project)"
)


# ============================================================
# LLM GENERATION CONFIGURATION
# ============================================================

MAX_OUTPUT_TOKENS = 1800

TEMPERATURE = 0.2


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_NAME = "CAP 931 Multi-Agent Sales Assistant"

APP_VERSION = "0.1.0"


# ============================================================
# DIRECTORY INITIALIZATION
# ============================================================

def create_project_directories() -> None:
    """
    Create runtime directories if they do not already exist.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# CONFIGURATION VALIDATION
# ============================================================

def validate_config() -> None:
    """
    Validate required application configuration.

    Raises:
        ValueError:
            If the OpenAI API key is missing.
    """

    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is missing.\n"
            "Add your OpenAI API key to the .env file."
        )

    if not OPENAI_MODEL:
        raise ValueError(
            "OPENAI_MODEL is missing.\n"
            "Add an OpenAI model name to the .env file."
        )


# ============================================================
# SAFE CONFIGURATION SUMMARY
# ============================================================

def get_config_summary() -> dict:
    """
    Return non-sensitive configuration information.

    The API key itself is intentionally never returned.
    """

    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "openai_model": OPENAI_MODEL,
        "api_key_configured": bool(OPENAI_API_KEY),
        "request_timeout": REQUEST_TIMEOUT,
        "max_web_text_chars": MAX_WEB_TEXT_CHARS,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "temperature": TEMPERATURE,
        "project_root": str(PROJECT_ROOT),
        "data_directory": str(DATA_DIR),
        "output_directory": str(OUTPUT_DIR),
    }


# ============================================================
# INITIALIZE PROJECT
# ============================================================

create_project_directories()