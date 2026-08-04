"""
Core business logic module for Mentor Report Generator.
Includes CSV loading, validation, analytics, recommendations,
chart rendering, image processing, PPTX generation, and AI assistant interface.
"""

from .csv_loader import CSVLoader
from .validator import DataValidator, ValidationResult
from .analytics import AnalyticsEngine, StudentAnalytics
from .recommendations import RecommendationEngine
from .charts import ChartGenerator
from .image_handler import ImageHandler
from .ppt_generator import PPTReportGenerator
from .ai_assistant import AIAssistantInterface

__all__ = [
    "CSVLoader",
    "DataValidator",
    "ValidationResult",
    "AnalyticsEngine",
    "StudentAnalytics",
    "RecommendationEngine",
    "ChartGenerator",
    "ImageHandler",
    "PPTReportGenerator",
    "AIAssistantInterface",
]
