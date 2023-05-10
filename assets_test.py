from Assets.FileHandling.Read import Read


def test_fileHandling():
    r = Read("Data/Defaults/test.json")
    assert r.extract() == {"test": True}