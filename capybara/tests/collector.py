import py.path
from _pytest.config import Config, PytestPluginManager, default_plugins
from _pytest.main import FSCollector


class GraftedSubSession(FSCollector):
    """
    Collects test files from outside of the file tree of the current pytest session.

    By default, pytest will only collect files from the directories with which it was
    invoked (or the current working directory, if none).

    With this, a "sub-session" may be collected from outside of the scope of the pytest
    session, e.g., in a third-party package.

    Args:
        name (str): The name of this grafted session.
        parent (Collector): The parent pytest collector.
        fspath (str): The directory from which files should be collected.
    """

    def __init__(self, name, parent, fspath):
        fspath = py.path.local(fspath)

        # Get a new configuration for our path, which may be outside of the
        # scope of the parent pytest session.
        config = _build_config_for_path(fspath)

        super(GraftedSubSession, self).__init__(fspath, parent=parent, config=config)

        # Use our given name, rather than the path-based name set by :class:`FSCollector`.
        self.name = name

    @property
    def gethookproxy(self):
        return self.session.gethookproxy

    @property
    def _fixturemanager(self):
        return self.session._fixturemanager

    def reportinfo(self):
        return self.fspath, None, ""

    def collect(self):
        self._fixturemanager.parsefactories(self)

        for path in self.fspath.visit(fil=lambda x: x.check(file=1),
                                      rec=self._recurse, bf=True, sort=True):
            for f in self._collectfile(path):
                yield f

    def _collectfile(self, path):
        ihook = self.gethookproxy(path)
        if ihook.pytest_ignore_collect(path=path, config=self.config):
            return ()
        return ihook.pytest_collect_file(path=path, parent=self)

    def _recurse(self, path):
        ihook = self.gethookproxy(path.dirpath())
        if ihook.pytest_ignore_collect(path=path, config=self.config):
            return
        ihook = self.gethookproxy(path)
        ihook.pytest_collect_directory(path=path, parent=self)
        return True


def _build_config_for_path(path):
    """
    Builds and returns a basic test configuration rooted at the given path.

    Args:
        path (LocalPath): The path to the files under test.

    Returns:
        Config: The generated test configuration.
    """

    # Find the root directory of the package containing our files.
    for rootdir in path.parts(reverse=True):
        if rootdir.join("setup.py").exists():
            break
    else:
        rootdir = path

    # Initialize a base configuration as pytest would.
    pluginmanager = PytestPluginManager()
    for spec in default_plugins:
        pluginmanager.import_plugin(spec)

    config = Config(pluginmanager)

    # Ensure that pytest sets its root directory (``config.rootdir``) to the
    # given path. If we don't, then using this configuration from outside of
    # this path will confuse pytest.
    args = [rootdir]

    config.parse(args)

    return config
