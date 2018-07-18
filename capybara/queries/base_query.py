import capybara


class BaseQuery(object):
    @staticmethod
    def normalize_wait(wait):
        """
        Returns the number of seconds to wait.

        Args:
            wait (int | float | bool, optional): The desired wait time in seconds, or ``False`` to
                disable waiting. Defaults to :data:`capybara.default_max_wait_time`.

        Returns:
            int: The number of seconds to wait.
        """

        if wait is not None:
            return wait or 0
        else:
            return capybara.default_max_wait_time
