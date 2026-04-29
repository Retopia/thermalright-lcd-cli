# SPDX-License-Identifier: Apache-2.0
# Copyright © 2025 Rejeb Ben Rejeb

import argparse


def main():
    parser = argparse.ArgumentParser(description="Thermalright LCD Control")
    parser.add_argument('--config',
                        required=True,
                        help="Display configuration file")
    args = parser.parse_args()
    from thermalright_lcd_control.common.logging_config import get_service_logger
    logger = get_service_logger()
    logger.info("Thermalright LCD Control starting in device controller mode")

    from thermalright_lcd_control.device_controller import run_service
    run_service(args.config)


if __name__ == "__main__":
    main()
