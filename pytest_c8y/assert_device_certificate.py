"""Device certificate assertions"""
import logging
from pytest_c8y.assert_device import AssertDevice


log = logging.getLogger()


class AssertDeviceCertificate(AssertDevice):
    """Assertions"""

    def delete_certificate(
        self,
        fingerprint: str,
        **kwargs,
    ) -> None:
        """Assert device certificate"""
        try:
            log.info("Removing device certificate. fingerprint=%s", fingerprint)
            self.context.client.delete(
                (
                    f"/tenant/tenants/{self.context.client.tenant_id}"
                    f"/trusted-certificates/{fingerprint}"
                ),
            )
        except KeyError as ex:
            log.warning("Certificate does not exist, so nothing to delete. ex=%s", ex)
        except ValueError as ex:
            log.error("Could not delete device certificate. ex=%s", ex)
            raise
        return
