import pytest


def test_basic_playbook(helpers):
    """test a basic playbook"""

    playbook = "playbook.yml"
    ## Given a basic playbook
    helpers.create_basic_playbook(playbook)

    ## When running the ansible playbook with the plugin
    span_list = helpers.run_ansible()
    
    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            helpers.assertGatheringFacts(span)
        if span["name"] == "hello world":
            helpers.assertCommonSpan(span)
            assert span["attributes"]["ansible.task.module"] == "debug"
            assert len(span["events"]) == 1
            assert len(span["attributes"]["ansible.task.args.name"]) == 1
            assert len(span["attributes"]["ansible.task.args.value"]) == 1
        if span["name"] == playbook:
            helpers.assertPlaybook(span)
    assert len(span_list) == 3


def test_playbook_with_long_output(helpers):
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
    span_list = helpers.run_ansible()

    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            helpers.assertGatheringFacts(span)
        if span["name"] == "Get build data":
            helpers.assertCommonSpan(span)
            assert span["attributes"]["ansible.task.module"] == "ansible.builtin.uri"
            assert len(span["events"]) == 1
            assert len(span["attributes"]["ansible.task.args.name"]) == 2
            assert len(span["attributes"]["ansible.task.args.value"]) == 2
        if span["name"] == playbook:
            helpers.assertPlaybook(span)
    assert len(span_list) == 3


def test_playbook_with_a_few_tasks(helpers):
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
    - name: bye world
      debug:
        msg: "bye world"
    - name: end world
      debug:
        msg: "end world"
""")

    ## When running the ansible playbook with the plugin
    span_list = helpers.run_ansible()

    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            helpers.assertGatheringFacts(span)
        if span["name"] == "Get build data":
            helpers.assertCommonSpan(span)
            assert span["attributes"]["ansible.task.module"] == "ansible.builtin.uri"
            assert len(span["events"]) == 1
            assert len(span["attributes"]["ansible.task.args.name"]) == 2
            assert len(span["attributes"]["ansible.task.args.value"]) == 2
        if span["name"] == playbook:
            helpers.assertPlaybook(span)
    assert len(span_list) == 5
