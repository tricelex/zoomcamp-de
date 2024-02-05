import pandas as pd


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake_case(column_name):
    result = ''.join(['_' + i.lower() if i.isupper() else i for i in column_name]).lstrip('_')
    return result

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    df_filtered = data[(data['passenger_count'] != 0) & (data['trip_distance'] != 0)]

    df_filtered['lpep_pickup_date'] = df_filtered['lpep_pickup_datetime'].dt.date

    df_filtered.columns = [camel_to_snake_case(col) for col in df_filtered.columns]

    return df_filtered


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
