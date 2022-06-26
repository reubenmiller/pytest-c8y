"""Binary assertions"""
import contextlib
import tempfile
from pathlib import Path

from c8y_api.model import Binary

from pytest_c8y.assert_device import AssertDevice


class Binaries(AssertDevice):
    """Binary assertions"""

    # pylint: disable=too-few-public-methods

    @contextlib.contextmanager
    def new_binary(
        self,
        name: str,
        binary_type: str = "",
        file: str = None,
        contents: str = None,
        **kwargs
    ):
        """Upload a binary and provide it to a context. The binary will be automatically
        deleted one it is done.

        with new_binary("myfile", file="./somefile.txt") as binary:
            binary.name
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            if file is None:
                file = Path(tmpdir) / name

                if isinstance(contents, str):
                    Path(file).write_text(contents, encoding="utf8")
                elif isinstance(contents, list):
                    Path(file).write_text("\n".join(contents), encoding="utf8")

            binary = Binary(
                self.context.client,
                type=binary_type,
                name=name,
                file=str(file),
                **kwargs
            ).create()
            try:
                yield binary
            finally:
                with contextlib.suppress(Exception):
                    binary.delete()
