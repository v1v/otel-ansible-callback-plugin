import pytest


def test_basic_playbook(helpers):
    """test a basic playbook"""

    playbook = "playbook.yml"
    ## Given a basic playbook
    helpers.create_basic_playbook(playbook)

    trace = "4bf92f3577b34da6a3ce929d0e0e4736"
    parent = "00f067aa0ba902b7"
    ## When running the ansible playbook with the plugin
    span_list = helpers.run_ansible_traceparent(f"00-{trace}-{parent}-01")
    
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
            helpers.assertPlaybook(span, f"0x{parent}")
            assert span["context"]["trace_id"] == f"0x{trace}"
    assert len(span_list) == 3
