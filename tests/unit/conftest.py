import pytest
import json
import subprocess


class Helpers:

    @staticmethod
    def run(command):
        output = "otel-output.json"
        p = subprocess.Popen(f"ANSIBLE_OPENTELEMETRY_STORE_SPANS_IN_FILE={output} {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        return Helpers.get_spans(output)


    @staticmethod
    def run_ansible(option = ""):
        return Helpers.run(f"{option} make run-test")


    @staticmethod
    def run_ansible_no_logs():
        return Helpers.run_ansible('ANSIBLE_OPENTELEMETRY_DISABLE_ATTRIBUTES_IN_LOGS=true')


    @staticmethod
    def run_ansible_hide_arguments():
        return Helpers.run_ansible('ANSIBLE_OPENTELEMETRY_HIDE_TASK_ARGUMENTS=true')
    

    @staticmethod
    def run_ansible_traceparent(traceparent):
        return Helpers.run_ansible(f"TRACEPARENT={traceparent}")


    @staticmethod
    def run_ansible_service(service):
        return Helpers.run_ansible(f"OTEL_SERVICE_NAME={service}")


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
    def get_spans(output):
        span_list = None
        with open(output, encoding="utf-8") as input:
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