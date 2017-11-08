import pytest
from jsonmodels import fields, models


def test_list_field_to_struct():
    field = fields.ListField()

    assert [1] == field.to_struct([1])
    assert [1, 2] == field.to_struct([1, 2])
    assert ["s"] == field.to_struct(["s"])
    assert ["s1", "s2"] == field.to_struct(["s1", "s2"])
    assert [1, "s"] == field.to_struct([1, "s"])


def test_list_field_parse_value_int():
    field = fields.ListField([int])

    assert [1] == field.parse_value([1])

    with pytest.raises(TypeError):
        field.parse_value(["s"])


def test_list_field_parse_value_str():
    field = fields.ListField([str])

    assert ["s"] == field.parse_value(["s"])

    with pytest.raises(TypeError):
        field.parse_value([1])


def test_list_field_parse_value_bool():
    field = fields.ListField([bool])

    assert [True] == field.parse_value([True])

    with pytest.raises(TypeError):
        field.parse_value([1])


def test_list_field():
    class ItemList(models.Base):
        items = fields.ListField([str, int])

    item_list = ItemList()
    item_list.items = [1, "s"]

    assert [1, "s"] == item_list.items
    assert {"items": [1, "s"]} == item_list.to_struct()
    # assert ItemList(**{"items": [1, "s"]}) == item_list
    assert [1, "s"] == item_list.items


def test_parse_list_field():
    import json
    from six import string_types

    fixture = """
    {
        "tags": ["tag_1", "tag_2"]
    }
    """

    class TagList(models.Base):
        tags = fields.ListField(string_types)

    tag_list_as_json = json.loads(fixture)
    tag_list = TagList(**tag_list_as_json)

    assert ["tag_1", "tag_2"] == tag_list.tags
