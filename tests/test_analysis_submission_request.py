import json
from copy import deepcopy

import pytest

from mythx_models.exceptions import ValidationError
from mythx_models.request import AnalysisSubmissionRequest

from .common import get_test_case

JSON_DATA, DICT_DATA = get_test_case("testdata/analysis-submission-request.json")
OBJ_DATA = AnalysisSubmissionRequest.from_json(JSON_DATA)


def assert_submission_request(req: AnalysisSubmissionRequest):
    DICT_DATA["analysisMode"] = (
        DICT_DATA["analysisMode"] if DICT_DATA["analysisMode"] != "full" else "standard"
    )
    assert req.contract_name == DICT_DATA["contractName"]
    assert req.bytecode == DICT_DATA["bytecode"]
    assert req.main_source == DICT_DATA["mainSource"]
    assert req.source_map == DICT_DATA["sourceMap"]
    assert req.deployed_bytecode == DICT_DATA["deployedBytecode"]
    assert req.deployed_source_map == DICT_DATA["deployedSourceMap"]
    assert req.sources == DICT_DATA["sources"]
    assert req.solc_version == DICT_DATA["version"]
    assert req.analysis_mode == DICT_DATA["analysisMode"]
    assert req.method == "POST"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {"data": DICT_DATA}


def test_analysis_submission_request_from_valid_json():
    req = AnalysisSubmissionRequest.from_json(JSON_DATA)
    assert_submission_request(req)


def test_analysis_submission_request_from_invalid_json():
    with pytest.raises(ValidationError):
        AnalysisSubmissionRequest.from_json("{}")


def test_analysis_submission_request_from_valid_dict():
    req = AnalysisSubmissionRequest.from_dict(DICT_DATA)
    assert_submission_request(req)


def test_analysis_submission_request_from_invalid_dict():
    with pytest.raises(ValidationError):
        AnalysisSubmissionRequest.from_dict({})


def test_analysis_submission_request_to_json():
    assert json.loads(OBJ_DATA.to_json()) == DICT_DATA


def test_analysis_submission_request_to_dict():
    assert OBJ_DATA.to_dict() == DICT_DATA


def test_analysis_submission_request_bytecode_only():
    req = AnalysisSubmissionRequest(bytecode=DICT_DATA["bytecode"])
    assert req.bytecode == DICT_DATA["bytecode"]
    assert req.analysis_mode == "quick"  # default value
    assert req.to_dict() == {"bytecode": DICT_DATA["bytecode"], "analysisMode": "quick"}
    assert json.loads(req.to_json()) == {
        "bytecode": DICT_DATA["bytecode"],
        "analysisMode": "quick",
    }


def test_analysis_submission_request_source_only():
    req = AnalysisSubmissionRequest(sources=DICT_DATA["sources"])
    assert req.sources == DICT_DATA["sources"]
    assert req.analysis_mode == "quick"  # default value
    assert req.to_dict() == {"sources": DICT_DATA["sources"], "analysisMode": "quick"}
    assert json.loads(req.to_json()) == {
        "sources": DICT_DATA["sources"],
        "analysisMode": "quick",
    }


def test_analysis_submission_request_invalid_mode():
    req = AnalysisSubmissionRequest(
        bytecode=DICT_DATA["bytecode"], analysis_mode="invalid"
    )
    with pytest.raises(ValidationError):
        req.to_dict()


def test_analysis_submission_request_missing_field():
    req = AnalysisSubmissionRequest()
    with pytest.raises(ValidationError):
        req.to_dict()


def test_key_without_extension():
    req = deepcopy(OBJ_DATA)
    OBJ_DATA.sources["noextensionhere"] = OBJ_DATA.sources.pop("PublicStorageArray.sol")
    OBJ_DATA.to_dict()  # trigger validation
