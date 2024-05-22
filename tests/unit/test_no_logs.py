import pytest


def test_basic_playbook(helpers):
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
    span_list = helpers.run_ansible_no_logs()
    
    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            helpers.assertGatheringFacts(span)
        if span["name"] == "hello world":
            helpers.assertCommonSpan(span)
            assert span["attributes"]["ansible.task.module"] == "debug"
            assert len(span["events"]) == 1
        if span["name"] == playbook:
            helpers.assertPlaybook(span)
    assert len(span_list) == 3
