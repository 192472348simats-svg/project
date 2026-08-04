from typing import Dict, Any, Optional
from .analytics import StudentAnalytics


class AIAssistantInterface:
    """
    Reserved interface for optional AI Writing Assistant module.
    
    CRITICAL RULE:
    The AI Writing Assistant MUST NEVER compute or alter attendance, risk scores,
    arrears, or academic statistics. It can only take an existing StudentAnalytics
    object and rewrite mentor comments into formal narrative text.
    """

    def __init__(self, api_key: Optional[str] = None, enabled: bool = False):
        self.api_key = api_key
        self.enabled = enabled

    def is_available(self) -> bool:
        """
        Returns whether AI Writing Assistant is enabled.
        Disabled by default for 100% offline core specification.
        """
        return self.enabled and bool(self.api_key)

    def rewrite_mentor_remarks(self, analytics: StudentAnalytics, raw_remarks: str) -> str:
        """
        Stub interface for AI mentor remark refinement.
        """
        if not self.is_available():
            # Return original remarks untouched with standard disclaimer
            return raw_remarks or "No remarks available."

        # Reserved logic for future LLM / API integration
        # Example prompt structure for future implementation:
        # prompt = f"Rewrite the following mentor remarks for {analytics.name} (Risk: {analytics.risk_level}): {raw_remarks}"
        return f"[AI Enhanced] {raw_remarks}"
