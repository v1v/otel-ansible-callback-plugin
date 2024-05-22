import pytest
import json
import subprocess


class Helpers:
    @staticmethod
    def run_ansible():
        p = subprocess.Popen('make run-test', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        return Helpers.get_spans()


    @staticmethod
    def run_ansible_no_logs():
        p = subprocess.Popen('ANSIBLE_OPENTELEMETRY_DISABLE_ATTRIBUTES_IN_LOGS=true make run-test', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        return Helpers.get_spans()
    

    @staticmethod
    def get_spans():
        span_list = None
        with open("otel-output.json", encoding="utf-8") as input:
            span_list = json.loads(input.read())['spans']
        return span_list


    @staticmethod
    def assertCommonSpan(span):
        assert span["kind"] == "SpanKind.INTERNAL"
        assert span["resource"]["attributes"]["service.name"] == "ansible"
        assert span["attributes"]["ansible.task.host.name"] == "localhost"
        assert span["attributes"]["ansible.task.host.status"] == "ok"
        assert span["parent_id"] is not None


    @staticmethod
    def assertGatheringFacts(span):
        assert span["status"]["status_code"] == "OK"
        Helpers.assertCommonSpan(span)


    @staticmethod
    def assertPlaybook(span):
        assert span["kind"] == "SpanKind.SERVER"
        assert span["status"]["status_code"] == "OK"
        assert span["parent_id"] is None


@pytest.fixture
def helpers():
    return Helpers