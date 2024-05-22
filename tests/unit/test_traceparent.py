import pytest


def test_basic_playbook(helpers):
    """test a basic playbook"""

    playbook = "playbook.yml"
    ## Given a basic playbook
    helpers.create_basic_playbook(playbook)

    ## When running the ansible playbook with the plugin
    span_list = helpers.run_ansible_traceparent()
    
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
            helpers.assertPlaybook(span, "0x00f067aa0ba902b7")
            assert span["context"]["trace_id"] == "0x4bf92f3577b34da6a3ce929d0e0e4736"
    assert len(span_list) == 3
