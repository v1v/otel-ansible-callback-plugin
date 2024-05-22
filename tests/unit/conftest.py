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
    def run_ansible_hide_arguments():
        p = subprocess.Popen('ANSIBLE_OPENTELEMETRY_HIDE_TASK_ARGUMENTS=true make run-test', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        return Helpers.get_spans()
    

    @staticmethod
    def run_ansible_traceparent(traceparent):
        p = subprocess.Popen(f"TRACEPARENT={traceparent} make run-test", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        return Helpers.get_spans()


    @staticmethod
    def run_ansible_service(service):
        p = subprocess.Popen(f"OTEL_SERVICE_NAME={service} make run-test", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        return Helpers.get_spans()


    @staticmethod
    def create_basic_playbook(playbook):
        with open(playbook, 'w', encoding="utf-8") as f:
            f.write("""---
- name: playbook
  hosts: localhost
  connection: local
  tasks:
    - name: hello world
      debug:
        msg: "hello world"
""")


    @staticmethod
    def get_spans():
        span_list = None
        with open("otel-output.json", encoding="utf-8") as input:
            span_list = json.loads(input.read())['spans']
        return span_list


    @staticmethod
    def assertCommonSpan(span, service = 'ansible'):
        assert span["kind"] == "SpanKind.INTERNAL"
        assert span["resource"]["attributes"]["service.name"] == service
        assert span["attributes"]["ansible.task.host.name"] == "localhost"
        assert span["attributes"]["ansible.task.host.status"] == "ok"
        assert span["parent_id"] is not None


    @staticmethod
    def assertGatheringFacts(span, service = 'ansible'):
        assert span["status"]["status_code"] == "OK"
        Helpers.assertCommonSpan(span, service)


    @staticmethod
    def assertPlaybook(span, trace = None):
        assert span["kind"] == "SpanKind.SERVER"
        assert span["status"]["status_code"] == "OK"
        assert span["parent_id"] == trace


@pytest.fixture
def helpers():
    return Helpers