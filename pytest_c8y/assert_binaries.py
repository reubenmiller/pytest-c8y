from pathlib import Path
import tempfile
from pytest_c8y.assert_device import AssertDevice
from c8y_api.model import Binary
import contextlib


class Binaries(AssertDevice):
    @contextlib.contextmanager
    def new_binary(
        self,
        name: str,
        binary_type: str = "",
        file: str = None,
        contents: str = None,
        **kwargs
    ):
        """Upload a binary and provide it to a context. The binary will be automatically deleted one it is done

        with new_binary("myfile", file="./somefile.txt") as binary:
            binary.name
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            if file is None:
                file = Path(tmpdir) / name

                if isinstance(contents, str):
                    Path(file).write_text(contents)
                elif isinstance(contents, list):
                    Path(file).write_text("\n".join(contents))

            binary = Binary(
                self.context.client, type=binary_type, name=name, file=file, **kwargs
            ).create()
            try:
                yield binary
            finally:
                with contextlib.suppress(Exception):
                    binary.delete()
