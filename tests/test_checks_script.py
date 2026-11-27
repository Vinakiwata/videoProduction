import copy

from conftest import write_yaml
from vp.checks import run_check

P = "01_script/script.yaml"


def _with(project, script):
    write_yaml(project / P, script)
    return project


def test_schema_pass(project):
    r = run_check("yaml_schema", project, {"path": P, "schema": "script"})
    assert r.status == "pass", r.evidence


def test_schema_fail_reports_location(project, good_script):
    bad = copy.deepcopy(good_script)
    del bad["scenes"][0]["segments"][0]["text"]
    r = run_check("yaml_schema", _with(project, bad), {"path": P, "schema": "script"})
    assert r.status == "fail"
    assert "scenes/0/segments/0" in r.evidence


def test_schema_missing_file_is_error(project):
    (project / P).unlink()
    r = run_check("yaml_schema", project, {"path": P, "schema": "script"})
    assert r.status == "error"


def test_unique_ids(project, good_script):
    assert run_check("script_unique_ids", project, {"path": P}).status == "pass"
    bad = copy.deepcopy(good_script)
    bad["scenes"][1]["segments"][0]["id"] = "S01-01"
    r = run_check("script_unique_ids", _with(project, bad), {"path": P})
    assert r.status == "fail" and "S01-01" in r.evidence


def test_source_refs(project, good_script):
    assert run_check("script_source_refs", project, {"path": P}).status == "pass"
    bad = copy.deepcopy(good_script)
    bad["scenes"][1]["segments"][1]["source_ids"] = ["SRC9"]
    r = run_check("script_source_refs", _with(project, bad), {"path": P})
    assert r.status == "fail" and "SRC9" in r.evidence


def test_no_placeholders(project, good_script):
    assert run_check("no_placeholders", project, {"path": P}).status == "pass"
    bad = copy.deepcopy(good_script)
    bad["scenes"][0]["segments"][0]["text"] = "Chỗ này TODO viết sau"
    r = run_check("no_placeholders", _with(project, bad), {"path": P})
    assert r.status == "fail" and "S01-01" in r.evidence


def test_segment_length(project, good_script):
    assert run_check("script_segment_length", project, {"path": P, "max_chars": 300}).status == "pass"
    bad = copy.deepcopy(good_script)
    bad["scenes"][0]["segments"][0]["text"] = "chữ " * 100
    r = run_check("script_segment_length", _with(project, bad), {"path": P, "max_chars": 300})
    assert r.status == "fail" and "S01-01" in r.evidence


def test_reading_speed(project, good_script):
    params = {"path": P, "min_sps": 2.5, "max_sps": 4.0}
    assert run_check("script_reading_speed", project, params).status == "pass"
    bad = copy.deepcopy(good_script)
    bad["scenes"][0]["segments"][0]["est_duration_s"] = 1  # 15 âm tiết / 1 giây
    r = run_check("script_reading_speed", _with(project, bad), params)
    assert r.status == "fail" and "S01-01" in r.evidence


def test_total_duration(project, good_script):
    params = {"path": P, "tolerance": 0.15}
    assert run_check("script_total_duration", project, params).status == "pass"
    bad = copy.deepcopy(good_script)
    bad["meta"]["target_duration_s"] = 60
    r = run_check("script_total_duration", _with(project, bad), params)
    assert r.status == "fail" and "29" in r.evidence


def test_brief_schema(project):
    r = run_check("yaml_schema", project, {"path": "00_brief/brief.yaml", "schema": "brief"})
    assert r.status == "pass", r.evidence


def test_file_exists(project):
    assert run_check("file_exists", project, {"paths": [P]}).status == "pass"
    r = run_check("file_exists", project, {"paths": [P, "nope.txt"]})
    assert r.status == "fail" and "nope.txt" in r.evidence


def test_unknown_check_is_error(project):
    assert run_check("khong_co", project, {}).status == "error"


def test_check_crash_becomes_error(project):
    # params sai kiểu -> không được làm sập tool, phải ra 'error'
    r = run_check("file_exists", project, {"paths": 123})
    assert r.status == "error"
