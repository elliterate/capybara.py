from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


def get_browser(browser_name, capabilities=None, config_obj=None):
    """
    Returns an instance of the given browser with the given capabilities and options.

    Args:
        browser_name (str): The name of the desired browser.
        capabilities (Dict[str, str | bool], optional): The desired capabilities of the browser. Defaults to None.
        config_obj (object, optional): An additional configuration object instance appropriate for the requested browser. (ChromeOptions, FirefoxProfile)

    Returns:
        WebDriver: An instance of the desired browser.
    """

    if browser_name == "chrome":
        return webdriver.Chrome(desired_capabilities=capabilities, chrome_options=config_obj)
    if browser_name == "edge":
        return webdriver.Edge(capabilities=capabilities)
    if browser_name in ["ff", "firefox"]:
        return webdriver.Firefox(capabilities=capabilities, firefox_profile=config_obj)
    if browser_name in ["ie", "internet_explorer"]:
        return webdriver.Ie(capabilities=capabilities)
    if browser_name == "phantomjs":
        return webdriver.PhantomJS(desired_capabilities=capabilities)
    if browser_name == "safari":
        return webdriver.Safari(desired_capabilities=capabilities)

    raise ValueError("unsupported browser: {}".format(repr(browser_name)))
