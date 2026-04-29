# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Rejeb Ben Rejeb

from typing import Any, Dict, Optional

import psutil

from thermalright_lcd_control.device_controller.metrics import Metrics
from thermalright_lcd_control.common.logging_config import LoggerConfig


class MemoryMetrics(Metrics):
    """System memory metrics."""

    def __init__(self):
        super().__init__()
        self.logger = LoggerConfig.setup_service_logger()
        self.ram_usage = None

    def get_temperature(self) -> Optional[float]:
        return None

    def get_usage_percentage(self) -> Optional[float]:
        try:
            self.ram_usage = float(psutil.virtual_memory().percent)
            return self.ram_usage
        except Exception as e:
            self.logger.error(f"Error reading RAM usage: {e}")
            return None

    def get_frequency(self) -> Optional[float]:
        return None

    def get_all_metrics(self) -> Dict[str, Any]:
        return {
            "usage_percentage": self.get_usage_percentage(),
        }

    def get_metric_value(self, metric_name) -> Any:
        if metric_name == "ram_usage":
            value = self.get_usage_percentage()
            return f"{value}" if value is not None else "N/A"
        return "N/A"

    def __str__(self) -> str:
        usage = self.get_usage_percentage()
        usage_s = f"{usage:.1f}%" if usage is not None else "N/A"
        return f"RAM - Usage: {usage_s}"
