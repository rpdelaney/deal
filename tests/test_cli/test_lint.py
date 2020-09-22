# built-in
from pathlib import Path

# project
from deal._cli._lint import get_errors, lint_command


TEXT = """
import deal

@deal.post(lambda x: x > 0)
def f(x):
    return -1
"""


def test_get_errors(tmp_path: Path):
    (tmp_path / 'example.py').write_text(TEXT)
    errors = list(get_errors(paths=[tmp_path]))
    assert len(errors) == 1
    assert errors[0]['code'] == 'DEAL012'
    assert errors[0]['content'] == '    return -1'


def test_lint_command(tmp_path: Path, capsys):
    (tmp_path / 'example.py').write_text(TEXT)
    count = lint_command([str(tmp_path)])
    assert count == 1

    captured = capsys.readouterr()
    assert 'return -1' in captured.out
    assert '(-1)' in captured.out
    assert '^' in captured.out


def test_lint_command_two_files(tmp_path: Path, capsys):
    (tmp_path / 'example1.py').write_text(TEXT)
    (tmp_path / 'example2.py').write_text(TEXT)
    count = lint_command([str(tmp_path)])
    assert count == 2

    captured = capsys.readouterr()
    assert 'example1.py' in captured.out
    assert 'example2.py' in captured.out
    assert 'return -1' in captured.out
    assert '(-1)' in captured.out
    assert '^' in captured.out


def test_lint_command_two_errors(tmp_path: Path, capsys):
    (tmp_path / 'example.py').write_text('from deal import pre\n' + TEXT)
    count = lint_command([str(tmp_path)])
    assert count == 2

    captured = capsys.readouterr()
    assert 'return -1' in captured.out
    assert '(-1)' in captured.out
    assert '^' in captured.out


def test_lint_command_json(tmp_path: Path, capsys):
    (tmp_path / 'example.py').write_text(TEXT)
    count = lint_command(['--json', str(tmp_path)])
    assert count == 1

    captured = capsys.readouterr()
    assert '"    return -1"' in captured.out
    assert '"-1"' in captured.out
    assert '^' not in captured.out
