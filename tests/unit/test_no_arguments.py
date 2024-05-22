import pytest


def test_basic_playbook(helpers):
    """test a basic playbook"""

    playbook = "playbook.yml"
    ## Given a basic playbook
    helpers.create_basic_playbook(playbook)

    ## When running the ansible playbook with the plugin
    span_list = helpers.run_ansible_hide_arguments()
    
    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            helpers.assertGatheringFacts(span)
        if span["name"] == "hello world":
            helpers.assertCommonSpan(span)
            assert span["attributes"]["ansible.task.module"] == "debug"
            assert "ansible.task.args.name" not in span["attributes"]
            assert "ansible.task.args.value" not in span["attributes"]
            assert len(span["events"]) == 1
        if span["name"] == playbook:
            helpers.assertPlaybook(span)
    assert len(span_list) == 3
