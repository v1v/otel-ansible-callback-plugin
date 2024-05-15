import pytest
import json
import subprocess


def get_spans():
    span_list = None
    with open("otel-output.json", encoding="utf-8") as input:
        span_list = json.loads(input.read())
    return span_list


def assertGatheringFacts(span):
    assert span["kind"] == "SpanKind.INTERNAL"
    assert span["status"]["status_code"] == "OK"
    assert span["resource"]["attributes"]["service.name"] == "ansible"
    assert span["attributes"]["ansible.task.host.name"] == "localhost"
    assert span["attributes"]["ansible.task.host.status"] == "ok"
    assert span["parent_id"] is not None
    return True


def assertPlaybook(span):
    assert span["kind"] == "SpanKind.SERVER"
    assert span["status"]["status_code"] == "OK"
    assert span["parent_id"] is None
    return True


def test_basic_playbook():
    """test a basic playbook"""

    playbook = "playbook.yml"
    ## Given a playbook
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

    ## When running the ansible playbook with the plugin
    p = subprocess.Popen('make run-test', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    span_list = get_spans()
    
    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            foundTestSuite = assertGatheringFacts(span)
        if span["name"] == playbook:
            foundTestSuite = assertPlaybook(span)
    assert True


def test_playbook_with_long_output():
    """test a basic playbook"""

    playbook = "playbook.yml"
    ## Given a playbook
    with open(playbook, 'w', encoding="utf-8") as f:
        f.write("""---
- name: playbook
  hosts: localhost
  connection: local
  tasks:
    - name: Get build data
      ansible.builtin.uri:
        url: "https://artifacts-api.elastic.co/v1/versions"
        validate_certs: no
""")

    ## When running the ansible playbook with the plugin
    p = subprocess.Popen('make run-test', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    span_list = get_spans()

    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            foundTestSuite = assertGatheringFacts(span)
        if span["name"] == playbook:
            foundTestSuite = assertPlaybook(span)
    assert True
