# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Rejeb Ben Rejeb

import argparse

from thermalright_lcd_control.common.logging_config import get_service_logger
from thermalright_lcd_control.device_controller.device_controller import run_service


def main():
    parser = argparse.ArgumentParser(description="Thermalright LCD Control")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to the display configuration directory",
    )
    args = parser.parse_args()

    logger = get_service_logger()
    logger.info("Thermalright LCD Control starting")
    run_service(args.config)


if __name__ == "__main__":
    main()
