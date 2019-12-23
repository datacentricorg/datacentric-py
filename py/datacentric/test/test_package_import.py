import importlib
import pkgutil
import unittest
from typing import List


def check_package(module_name: str) -> List[str]:
    """Check package for import errors."""
    errors: List[str] = []
    try:
        module_ = __import__(module_name)
    except ImportError as error:
        raise Exception(f'Cannot import module: {error.name}. Check sys.path')

    packages = list(pkgutil.walk_packages(path=module_.__path__, prefix=module_.__name__ + '.'))
    modules = [x for x in packages if not x.ispkg]
    for m in modules:
        try:
            importlib.import_module(m.name)
        except SyntaxError as error:
            errors.append(f'Cannot import module: {m.name}. Error: {error.msg}. Line: {error.lineno}, {error.offset}')
            continue
        except NameError as error:
            errors.append(f'Cannot import module: {m.name}. Error: {error.args}')

    return errors


class PackageImportTest(unittest.TestCase):
    """Checks that all modules of package are imprortable."""

    def test_datacentric(self):
        errors = check_package('datacentric')
        if errors:
            print('\n'.join(errors))
        self.assertEqual(0, len(errors))


if __name__ == '__main__':
    unittest.main()
