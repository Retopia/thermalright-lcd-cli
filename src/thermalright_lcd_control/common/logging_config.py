# SPDX-License-Identifier: Apache-2.0
# Copyright © 2025 Rejeb Ben Rejeb

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggerConfig:
    """Centralized logging configuration for the project."""

    SERVICE_LOG_FILE = "/var/log/thermalright-lcd-control-service.log"

    @staticmethod
    def is_development_mode():
        """Detect whether the application is running from a source checkout."""
        current_file = Path(__file__).resolve()
        if "src" in current_file.parts:
            return True

        system_paths = ["/usr", "/opt", "/var"]
        if any(str(current_file).startswith(path) for path in system_paths):
            return False

        if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
            venv_path = Path(sys.prefix)
            project_path = current_file.parent.parent.parent
            try:
                venv_path.relative_to(project_path)
                return True
            except ValueError:
                pass

        return os.getenv("THERMALRIGHT_DEV_MODE", "").lower() in ("1", "true", "yes")

    @staticmethod
    def _create_console_handler():
        """Create a console handler."""
        try:
            import colorlog

            handler = colorlog.StreamHandler()
            handler.setFormatter(colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                }
            ))
        except ImportError:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

        return handler

    @staticmethod
    def _create_file_handler(log_file_path):
        """Create a rotating file handler."""
        log_file = Path(log_file_path)
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
            )
            handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
            return handler
        except (PermissionError, OSError):
            return LoggerConfig._create_console_handler()

    @staticmethod
    def setup_service_logger():
        """Setup logger for the device controller."""
        logger = logging.getLogger("thermalright.device_controller")
        logger.handlers.clear()

        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

        if LoggerConfig.is_development_mode():
            handler = LoggerConfig._create_console_handler()
            logger.info("Device controller logger configured for development mode (console)")
        else:
            handler = LoggerConfig._create_file_handler(LoggerConfig.SERVICE_LOG_FILE)
            logger.info(
                f"Device controller logger configured for production mode (file: {LoggerConfig.SERVICE_LOG_FILE})"
            )

        logger.addHandler(handler)
        logger.propagate = False
        return logger


def get_service_logger():
    """Get the device controller logger instance."""
    return LoggerConfig.setup_service_logger()
