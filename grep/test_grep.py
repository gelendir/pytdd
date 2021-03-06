import pytest

from grep import grep


class FileUtil(object):

    def __init__(self, tmpdir):
        self.tmpdir = tmpdir

    def create_file(self, name, contents):
        path = self.tmpdir.join(name)
        path.write(contents)
        return str(path)


@pytest.fixture
def fileutil(tmpdir):
    return FileUtil(tmpdir)


def test_given_empty_file_when_empty_pattern_then_prints_nothing(capsys, fileutil):
    path = fileutil.create_file('emptyfile', '')

    grep('', path)

    out, err = capsys.readouterr()
    assert out == "\n"


def test_given_file_with_a_line_when_empty_pattern_then_prints_line(capsys, fileutil):
    path = fileutil.create_file('oneline', 'one line')

    grep('', path)

    out, err = capsys.readouterr()
    assert 'one line' in out


def test_given_file_with_two_lines_when_pattern_contains_a_line_then_prints_line(capsys, fileutil):
    path = fileutil.create_file('twolines', 'a\nb\n')

    grep('b', path)

    out, err = capsys.readouterr()
    assert 'b' in out
    assert 'a' not in out


def test_given_2_files_when_grepping_then_prints_lines_in_all_files(capsys, fileutil):
    first_file = fileutil.create_file('first', 'aa\nbb\n')
    second_file = fileutil.create_file('second', 'ab\nbc\n')

    grep('a', first_file, second_file)

    out, err = capsys.readouterr()
    assert 'aa' in out
    assert 'ab' in out


def test_given_file_when_using_regex_then_prints_matching_lines(capsys, fileutil):
    path = fileutil.create_file('file', 'a\n1\nb\n2\n')

    grep('[12]', path)

    out, err = capsys.readouterr()
    assert '1' in out
    assert '2' in out


def test_given_option_ignore_case_when_matching_capital_letters_then_prints_matching_lines(capsys, fileutil):
    path = fileutil.create_file('uppercase', 'A\nb\n')

    grep('a|b', path, ignore_case=True)

    out, err = capsys.readouterr()
    assert 'A' in out
    assert 'b' in out


def test_given_option_print_line_number_when_grepping_then_prints_line_numbers(capsys, fileutil):
    path = fileutil.create_file('line_numbers', 'a\nb\naa\nbb\n')

    grep('a', path, line_number=True)

    out, err = capsys.readouterr()
    assert '1:a' in out
    assert '3:aa' in out


def test_given_empty_lines_when_grepping_does_not_print_additional_lines(capsys, fileutil):
    path = fileutil.create_file('empty_lines', 'a\n\na\n')

    grep('a', path)

    out, err = capsys.readouterr()
    assert out == 'a\na\n'
