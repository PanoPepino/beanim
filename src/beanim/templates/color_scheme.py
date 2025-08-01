import importlib

from ..my_imports import *

__all__ = ["import_template"]


def import_template(module_name: str):
    """
    Import a chosen template to standardize styling across all Beanim objects.

    This function loads a predefined color and styling template that will be applied
    to all subsequent Beanim objects created in the scene. It helps maintain visual
    consistency across presentations.

    :param module_name: Name of the template to import. Must be one of the allowed templates.
    :type module_name: str

    :raises ModuleNotFoundError: If the specified template module cannot be found.

    .. note::

       This function should be called before defining your Scene class to ensure
       the template is properly loaded before any Beanim objects are created.

    **Available templates:**
        - ``"fancy_mint"``
        - ``"blue_ice"``
        - ``"fire_autumn"``
        - ``"default_template"`` (fallback)

    **Example usage:**

    .. code-block:: python

        from beanim import *

        import_template('desired_template')

        class MyScene(Scene):
            def construct(self):
                # Your Beanim objects will now use the selected template
                pass
    """
    allowed_modules = ["fancy_mint", "blue_ice", "fire_autumn"]

    # Import base template
    if module_name in allowed_modules:
        module_path = f"beanim.templates.collection.{module_name}"
        print("Using " + f'{module_name}' + " template!!")
    else:
        print("That template does not exist. Using default B/W template instead!!")
        module_path = "beanim.templates.collection.default_template"

    importlib.import_module(module_path)
