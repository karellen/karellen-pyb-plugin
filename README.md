# Karellen PyBuilder Plugin

[Karellen](https://www.karellen.co/karellen/) [PyBuilder](http://pybuilder.github.io/) Plugin

This is the main PyBuilder plugin for all of the projects under [Karellen](https://www.karellen.co/) umbrella. 
This plugin governs the following PyBuilder project settings:

1. Code style and copyright headers.
2. Unit and integration test passing threshold.
3. Documentation building and style.
4. Code packaging, packaging metadata and signing.

In order to make sure your project conforms to Karellen standards, use this plugin by adding the following to your `build.py`: 

```python

from pybuilder.core import use_plugin 

# ... #

use_plugin("pypi:karellen_pyb_plugin", ">=0.0.1.dev")

```

## For Developers

[Karellen PyBuilder Plugin Issue Tracker](https://waffle.io/karellen/karellen)

[Karellen PyBuilder Plugin Source Code](https://github.com/karellen/karellen-pyb-plugin)
