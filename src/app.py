import logging
import os
import configargparse

from vk_parser import get_comments
from utils import save_to_csv
from extractor.main import extract

_logger = logging.getLogger(__name__)


def setup_logging(loglevel: str = "DEBUG", logfile: str = None) -> None:
    """
    Sets up logging handlers and a format

    :param logfile:
    :param loglevel:
    """
    loglevel = getattr(logging, loglevel)

    logger = logging.getLogger()
    logger.setLevel(loglevel)
    fmt = (
        "%(asctime)s: %(levelname)s: %(filename)s: "
        + "%(funcName)s(): %(lineno)d: %(message)s"
    )
    formatter = logging.Formatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if logfile is not None:
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    logging.getLogger("vkbottle").setLevel(logging.WARNING)


if __name__ == "__main__":
    setup_logging()
    parser = configargparse.ArgumentParser(default_config_files=[os.path.join(os.path.dirname(__file__), ".env")])
    parser.add_argument("--vk_token", env_var="VK_TOKEN", dest="vk_token", type=str, help="VK API token")
    args = parser.parse_args()

    save_pth = "/data"
    raw_comments_path = os.path.join(save_pth, "comments.csv")
    result_comments_path = os.path.join(save_pth, "result.")

    comments_list = get_comments(args.vk_token)

    if len(comments_list) > 0:
        save_to_csv(data=comments_list, file_path=raw_comments_path)
    else:
        _logger.warning("No parsed comments")
        exit()

    extract(raw_comments_path, save_pth)

    logging.info(f"Exported {len(comments_list)} comments total")
