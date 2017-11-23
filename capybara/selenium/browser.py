from selenium import webdriver


def get_browser(browser_name, capabilities=None, **options):
    """
    Returns an instance of the given browser with the given capabilities.

    Args:
        browser_name (str): The name of the desired browser.
        capabilities (Dict[str, str | bool], optional): The desired capabilities of the browser.
            Defaults to None.
        options: Arbitrary keyword arguments for the browser-specific subclass of
            :class:`webdriver.Remote`.

    Returns:
        WebDriver: An instance of the desired browser.
    """

    if browser_name == "chrome":
        return webdriver.Chrome(desired_capabilities=capabilities, **options)
    if browser_name == "edge":
        return webdriver.Edge(capabilities=capabilities, **options)
    if browser_name in ["ff", "firefox"]:
        return webdriver.Firefox(capabilities=capabilities, **options)
    if browser_name in ["ie", "internet_explorer"]:
        return webdriver.Ie(capabilities=capabilities, **options)
    if browser_name == "phantomjs":
        return webdriver.PhantomJS(desired_capabilities=capabilities, **options)
    if browser_name == "remote":
        return webdriver.Remote(desired_capabilities=capabilities, **options)
    if browser_name == "safari":
        return webdriver.Safari(desired_capabilities=capabilities, **options)

    raise ValueError("unsupported browser: {}".format(repr(browser_name)))
