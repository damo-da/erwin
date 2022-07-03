def test_import():
    import solver
    from os import getenv

    print("OUTPUT", getenv("PYTHONPATH"))

