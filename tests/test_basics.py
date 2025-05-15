"""When I hacks this bad, I write tests."""

import pytest
import platform

from pathlib import Path

from uvtrick import Env, load

hello = load("tests/rich-script.py", "hello")
add = load("tests/rich-script.py", "add")


def test_smoke():
    assert hello() == 1


def test_args():
    assert add(1, 2) == 3
    assert add(a=1, b=4) == 5


def test_no_exist():
    with pytest.raises(ValueError):
        func = load("tests/rich-script.py", "no_exist")
        func()


def test_no_metadata():
    with pytest.raises(ValueError):
        func = load("tests/rich-fail.py", "add")
        func()


def test_env_works1():
    def uses_rich(a, b):
        from rich import print

        print("hello")
        return a + b

    for version in ["13", "12"]:
        assert Env(f"rich=={version}").run(uses_rich, a=1, b=2) == 3


def test_env_works2():
    def handles_all_types(arr, dictionary, string):
        return {"arr": arr, "dictionary": dictionary, "string": string}

    for version in ["13", "12"]:
        out = Env(f"rich=={version}").run(
            handles_all_types,
            arr=[1, 2, 3],
            dictionary={"a": 1, "b": 2},
            string="hello",
        )
        assert out == {
            "arr": [1, 2, 3],
            "dictionary": {"a": 1, "b": 2},
            "string": "hello",
        }

def test_path_escape():
    
    def helper(path_base: str) -> None:
        file_in  = path_base + r"pickled_inputs.pickle"
        file_out = path_base + r"tmp.pickle"
    
        e = Env("")
        e.temp_dir = Path(path_base)
    
        def func():
            print('me')
    
        assert file_in  in e.maincall(func)
        assert file_out in e.maincall(func)

    if platform.system() == "Windows":
        helper(r'C:\\win\\path\\big\\')
        helper(r'd:\\win\\path\\small\\')
    else:
        helper(r'/linux/path/')

