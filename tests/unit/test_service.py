import pytest


def test_basic_playbook(helpers):
    """test a basic playbook"""

    playbook = "playbook.yml"
    ## Given a basic playbook
    helpers.create_basic_playbook(playbook)

    ## When running the ansible playbook with the plugin
    span_list = helpers.run_ansible_service("acme")
    
    ## Then
    for span in span_list:
        if span["name"] == "Gathering Facts":
            helpers.assertGatheringFacts(span, "acme")
        if span["name"] == "hello world":
            helpers.assertCommonSpan(span, "acme")
            assert span["attributes"]["ansible.task.module"] == "debug"
            assert len(span["events"]) == 1
            assert len(span["attributes"]["ansible.task.args.name"]) == 1
            assert len(span["attributes"]["ansible.task.args.value"]) == 1
        if span["name"] == playbook:
            helpers.assertPlaybook(span)
    assert len(span_list) == 3
