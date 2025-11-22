import logging


def config_logs(verbose: bool = False):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class LoggingMixin:
    _log: logging.Logger | None = None

    @property
    def log(self) -> logging.Logger:
        if self._log is None:
            name = self.__class__.__name__
            self._log = logging.getLogger(name)
        return self._log
