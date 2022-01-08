"""
Utility class to enable simpler imports
"""

from ..builtin.integration.mixins import AppMixin, SettingsMixin, ScheduleMixin, UrlsMixin, NavigationMixin, APICallMixin

__all__ = [
    'AppMixin',
    'NavigationMixin',
    'ScheduleMixin',
    'SettingsMixin',
    'UrlsMixin',
    'APICallMixin',
]
